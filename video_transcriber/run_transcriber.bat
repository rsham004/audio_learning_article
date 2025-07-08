@echo off
REM Set the AssemblyAI API key as an environment variable
REM Replace YOUR_ASSEMBLYAI_API_KEY with your actual API key
set ASSEMBLYAI_API_KEY=579bb999c2234de0921a01ce336d71da

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
pause

:end
