@echo off
echo ============================================================
echo INSTALLING DEPENDENCIES - User Activity Logger
echo ============================================================
echo.

echo [1/3] Installing Python packages for activity tracking...
pip install pynput psutil pygetwindow pywin32 schedule
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python packages
    pause
    exit /b 1
)
echo.

echo [2/3] Installing FastAPI and Uvicorn for API server...
pip install fastapi "uvicorn[standard]"
if %errorlevel% neq 0 (
    echo ERROR: Failed to install API packages
    pause
    exit /b 1
)
echo.

echo [3/3] Installing Node.js packages for frontend...
cd web
echo Removing old node_modules...
if exist node_modules rmdir /s /q node_modules
echo Installing fresh dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node packages
    cd ..
    pause
    exit /b 1
)
echo.
echo Installing Tailwind CSS v3...
call npm install -D tailwindcss@^3.4.0 postcss autoprefixer
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Tailwind CSS
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

echo ============================================================
echo SUCCESS: All dependencies installed!
echo ============================================================
echo.
echo Next Steps:
echo 1. Edit reports\confiq.py and set START_TIME
echo 2. Run AUTO_START_ALL.bat
echo 3. Open http://localhost:5173
echo 4. Login with: andrewtatecoder@gmail.com
echo.
pause
