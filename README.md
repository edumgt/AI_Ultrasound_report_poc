# Ultrasound Auto Report PoC (Windows / Python)

## 1) Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 2) Run
```bash
python app.py
```

## 3) Notes
- 기본 STT는 faster-whisper (로컬) 입니다.
- 모델 다운로드가 처음에 발생할 수 있습니다(환경에 따라 시간이 걸림).
- assets/terms.json 의 aliases 품질이 '용어 정확도'를 좌우합니다.
- data/sessions/ 아래에 세션 결과(raw/corrected/report/structured)가 저장됩니다.
