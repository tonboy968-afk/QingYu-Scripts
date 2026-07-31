@echo off
setlocal

echo ========================================
echo   Kefu Script Manager - Starting...
echo ========================================
echo.

cd /d "%~dp0backend"

if not exist "app\main.py" (
    echo [ERROR] Cannot find backend/app/main.py. Please run this script in the project root.
    pause
    exit /b 1
)

echo [1/2] Starting backend service on port 8010...
echo Please check the 'KefuScriptBackend' window for service logs.

start "KefuScriptBackend" cmd /k "python -m uvicorn app.main:app --host 127.0.0.1 --port 8010 --reload"

echo [2/2] Waiting for service to start...
timeout /t 3 > nul

echo Opening browser...
start "" http://127.0.0.1:8010

echo ========================================
echo   Started successfully!
echo   - Backend logs are in the 'KefuScriptBackend' window.
echo   - The system interface is opened in your browser.
echo   - Close the backend window to stop the service.
echo ========================================
echo.
pause
