@echo off
echo Audio Learning Article - Enhanced Video Transcriber
echo ===================================================
echo Features: Video transcription + AI learning article generation
echo.

REM Check if API keys are set as environment variables
if "%ASSEMBLYAI_API_KEY%"=="" (
    echo ERROR: ASSEMBLYAI_API_KEY environment variable is not set.
    echo Please set your AssemblyAI API key as an environment variable:
    echo   set ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
    echo.
    echo Or add it to your system environment variables.
    pause
    exit /b 1
)

if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY environment variable is not set.
    echo Please set your Google Gemini API key as an environment variable:
    echo   set GEMINI_API_KEY=your_gemini_api_key_here
    echo.
    echo Or add it to your system environment variables.
    pause
    exit /b 1
)

echo ✓ API keys found in environment variables
echo.

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
