from __future__ import annotations
import os, time, queue as pyqueue
import numpy as np

def stt_worker_main(out_q, ctrl_q, cfg: dict):
    """
    Runs in a separate PROCESS to isolate native crashes from the Qt UI process.
    - Captures mic audio with sounddevice
    - Transcribes with faster-whisper
    - Sends recognized text chunks to UI through out_q
    """
    # Make native path conservative
    os.environ.setdefault("CT2_FORCE_CPU_ISA", "GENERIC")

    # Imports inside process (important on Windows spawn)
    import sounddevice as sd
    from faster_whisper import WhisperModel

    sample_rate = int(cfg.get("sample_rate", 16000))
    block_ms = int(cfg.get("block_ms", 500))
    blocksize = int(sample_rate * (block_ms / 1000.0))

    model_size = cfg.get("model_size", "tiny")
    device = cfg.get("device", "cpu")
    compute_type = cfg.get("compute_type", "int8")
    beam_size = int(cfg.get("beam_size", 1))
    vad_filter = bool(cfg.get("vad_filter", False))
    language = cfg.get("language", None)
    initial_prompt = cfg.get("initial_prompt", "")

    out_q.put({"type": "status", "msg": f"Loading STT model ({model_size}) in subprocess..."})
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    out_q.put({"type": "status", "msg": "STT model loaded."})

    audio_q: "pyqueue.Queue[np.ndarray]" = pyqueue.Queue()

    running = True

    def callback(indata, frames, t, status):
        # Never raise in callback; just enqueue
        try:
            audio = np.squeeze(indata.copy()).astype(np.float32)
            audio_q.put(audio)
        except Exception as e:
            try:
                out_q.put({"type": "error", "msg": f"audio callback error: {e}"})
            except Exception:
                pass

    stream = sd.InputStream(
        channels=1,
        samplerate=sample_rate,
        blocksize=blocksize,
        dtype="float32",
        callback=callback,
    )
    stream.start()
    out_q.put({"type": "status", "msg": "Listening (subprocess)..."})

    buffer = []
    target_samples = int(sample_rate * 1.5)

    try:
        while running:
            # Stop command?
            try:
                cmd = ctrl_q.get_nowait()
                if cmd == "STOP":
                    running = False
                    break
            except Exception:
                pass

            try:
                chunk = audio_q.get(timeout=0.2)
                buffer.append(chunk)

                if sum(len(x) for x in buffer) >= target_samples:
                    audio = np.concatenate(buffer).astype(np.float32)
                    buffer.clear()

                    segments, _info = model.transcribe(
                        audio,
                        language=language,
                        beam_size=beam_size,
                        vad_filter=vad_filter,
                        initial_prompt=initial_prompt,
                    )
                    parts = []
                    for seg in segments:
                        if seg.text:
                            parts.append(seg.text.strip())
                    text = " ".join(parts).strip()
                    if text:
                        out_q.put({"type": "text", "text": text})

            except pyqueue.Empty:
                pass
            except Exception as e:
                out_q.put({"type": "error", "msg": f"stt error: {e}"})
                time.sleep(0.1)
    finally:
        try:
            stream.stop()
            stream.close()
        except Exception:
            pass
        out_q.put({"type": "status", "msg": "Stopped (subprocess)."})
