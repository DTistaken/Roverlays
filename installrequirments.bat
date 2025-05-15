@echo off
echo Installing required Python packages...

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Upgrade pip just in case
python -m pip install --upgrade pip

REM Install required packages
python -m pip install PyQt5 psutil pynput GPUtil

echo All packages installed successfully.
pause
