const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const uploadBtn = document.getElementById('uploadBtn');
const statusEl = document.getElementById('status');
const transcriptEl = document.getElementById('transcript');
const player = document.getElementById('player');
const serverResponseEl = document.getElementById('serverResponse');

let mediaRecorder;
let mediaStream;
let audioChunks = [];
let recordedBlob = null;
let recognition;

const setStatus = (msg) => {
  statusEl.textContent = msg;
};

const initSpeechRecognition = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    setStatus('브라우저 음성 인식을 지원하지 않습니다.');
    return null;
  }

  const rec = new SpeechRecognition();
  rec.lang = 'ko-KR';
  rec.continuous = true;
  rec.interimResults = true;

  rec.onresult = (event) => {
    let text = '';
    for (let i = 0; i < event.results.length; i += 1) {
      text += event.results[i][0].transcript + ' ';
    }
    transcriptEl.value = text.trim();
  };

  rec.onerror = (event) => {
    setStatus(`음성 인식 오류: ${event.error}`);
  };

  return rec;
};

startBtn.addEventListener('click', async () => {
  try {
    transcriptEl.value = '';
    audioChunks = [];
    recordedBlob = null;

    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(mediaStream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
      player.src = URL.createObjectURL(recordedBlob);
      uploadBtn.disabled = false;
    };

    mediaRecorder.start();
    recognition = initSpeechRecognition();
    if (recognition) recognition.start();

    setStatus('녹음 중...');
    startBtn.disabled = true;
    stopBtn.disabled = false;
  } catch (err) {
    setStatus(`마이크 접근 실패: ${err.message}`);
  }
});

stopBtn.addEventListener('click', () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
  }

  if (mediaStream) {
    mediaStream.getTracks().forEach((track) => track.stop());
  }

  if (recognition) {
    recognition.stop();
  }

  setStatus('녹음 종료');
  startBtn.disabled = false;
  stopBtn.disabled = true;
});

uploadBtn.addEventListener('click', async () => {
  if (!recordedBlob) {
    setStatus('업로드할 녹음 파일이 없습니다.');
    return;
  }

  const form = new FormData();
  form.append('audio', recordedBlob, 'recorded_audio.webm');
  form.append('transcript', transcriptEl.value);

  try {
    const res = await fetch('/api/upload-audio/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': window.CSRF_TOKEN,
      },
      body: form,
    });

    const data = await res.json();
    serverResponseEl.textContent = JSON.stringify(data, null, 2);
    setStatus(data.ok ? '서버 업로드 완료' : '업로드 실패');
  } catch (err) {
    setStatus(`업로드 오류: ${err.message}`);
  }
});
