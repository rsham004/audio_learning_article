@echo off
echo Audio Learning Article - Enhanced Video Transcriber
echo ===================================================
echo Features: Video transcription + AI learning article generation
echo.

REM Check if API keys are set as environment variables
REM Removed API key checks - now loaded via .env

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Try to run with python, then python3, then py
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using Python executable: python
    python process_videos.py
    goto :end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using Python executable: python3
    python3 process_videos.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Using Python executable: py
    py process_videos.py
    goto :end
)

echo Error: Python not found. Please install Python or add it to your PATH.
echo.
echo Required Python packages:
echo - assemblyai
echo - google-generativeai
echo - pydub (optional)
echo.
echo Install with: pip install assemblyai google-generativeai pydub
pause

:end
