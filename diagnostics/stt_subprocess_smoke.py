import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import multiprocessing as mp
import time, os
from core.stt_process import stt_worker_main

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    out_q = mp.Queue()
    ctrl_q = mp.Queue()
    cfg = dict(model_size="tiny", device="cpu", compute_type="int8", beam_size=1, vad_filter=False, sample_rate=16000, block_ms=500)

    p = mp.Process(target=stt_worker_main, args=(out_q, ctrl_q, cfg), daemon=True)
    p.start()
    t0 = time.time()
    try:
        while time.time() - t0 < 10:
            while not out_q.empty():
                print(out_q.get())
            time.sleep(0.2)
    finally:
        ctrl_q.put("STOP")
        p.join(3)
        if p.is_alive():
            p.terminate()
        print("done")