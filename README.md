# Ultrasound Auto Report PoC (Windows)

## Key change (stability)
STT + microphone capture runs in a **separate subprocess** to avoid Qt(QThread) + native library crashes (0xC0000005).

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```powershell
python app.py
```

## Usage
- F2: Start/Stop (starts STT subprocess)
- F3: Reset
- Ctrl+Enter: Generate report
- Ctrl+S: Save session

## Diagnostics
Run subprocess-only STT smoke test (10 seconds):
```powershell
python .\diagnostics\stt_subprocess_smoke.py
```
