@echo off

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

cls
echo ============================================================
echo   EMPLOYEE ACTIVITY MONITOR - STARTING...
echo ============================================================
echo.

echo Adding firewall rules for phone access...
netsh advfirewall firewall delete rule name="Activity Logger Web" >nul 2>&1
netsh advfirewall firewall delete rule name="Activity Logger API" >nul 2>&1
netsh advfirewall firewall add rule name="Activity Logger Web" dir=in action=allow protocol=TCP localport=5173 >nul 2>&1
netsh advfirewall firewall add rule name="Activity Logger API" dir=in action=allow protocol=TCP localport=8000 >nul 2>&1
echo Firewall configured for network access.
echo.

echo Cleaning up old processes...
taskkill /F /FI "WINDOWTITLE eq API Server*" 2>nul
taskkill /F /FI "WINDOWTITLE eq React Dashboard*" 2>nul
taskkill /F /FI "WINDOWTITLE eq Activity Logger*" 2>nul

REM Kill processes on ports
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do taskkill /F /PID %%a 2>nul

timeout /t 2 /nobreak >nul

echo [1/3] Starting API Server...
start "API Server" cmd /k "cd /d %~dp0api && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 5 /nobreak >nul

echo [2/3] Starting React Dashboard...
start "React Dashboard" cmd /k "cd /d %~dp0web && parcel index.html --port 5173"
timeout /t 8 /nobreak >nul

echo [3/3] Starting Activity Logger...
start "Activity Logger" cmd /k "cd /d %~dp0 && python main.py"

echo.
echo ============================================================
echo   ALL SERVICES STARTED!
echo ============================================================
echo.
echo WAIT 15 SECONDS, then open:
echo   On PC: http://localhost:5173
echo   On Phone: http://192.168.29.210:5173
echo.
echo Login: andrewtatecoder@gmail.com
echo.
echo Note: PC and phone must be on same WiFi network
echo.
pause
