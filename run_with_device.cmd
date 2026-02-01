@echo off
REM Change the number to your input device index (see diagnostics\list_devices.py)
set INPUT_DEVICE=1
python app.py
echo ExitCode=%ERRORLEVEL%
pause
