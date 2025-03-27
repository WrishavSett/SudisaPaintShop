@echo off

net session >nul 2>&1
if %errorlevel% neq 0 (
    :: Relaunch with elevated privileges
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

REM Change to the D: drive
D:

REM Navigate to the Camduc-Sudisa directory
cd Camduc-Sudisa

REM Activate the virtual environment
call virtualenv\Scripts\activate

REM Run the Django server in a new PowerShell process
start powershell -NoProfile -Command "Start-Process -NoNewWindow -FilePath 'python' -ArgumentList 'manage.py runserver'"

REM Wait for 5 seconds
timeout /t 2 /nobreak > nul

REM Open the URL in the default web browser
start http://127.0.0.1:8000/ai/home
