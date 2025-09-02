@echo off
echo 🚀 Starting Task-Automator Pro Local Development Server
echo ==================================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

REM Check Node.js version
for /f "tokens=1,2 delims=." %%a in ('node --version') do set NODE_VERSION=%%a
set NODE_VERSION=%NODE_VERSION:~1%
if %NODE_VERSION% lss 18 (
    echo ❌ Node.js version 18+ is required. Current version: 
    node --version
    pause
    exit /b 1
)

echo ✅ Node.js version: 
node --version

REM Check if .env.local exists
if not exist .env.local (
    echo 📝 Creating .env.local from template...
    copy .env.local.example .env.local
    echo ✅ .env.local created. Please review and update if needed.
)

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo 📦 Installing dependencies...
    npm install
    echo ✅ Dependencies installed.
) else (
    echo ✅ Dependencies already installed.
)

REM Build frontend if dist doesn't exist
if not exist client\dist (
    echo 🔨 Building frontend...
    npm run build
    echo ✅ Frontend built.
) else (
    echo ✅ Frontend already built.
)

echo.
echo 🌐 Starting development server...
echo 📱 Frontend will be available at: http://localhost:5000
echo 🔌 API will be available at: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the development server
npm run dev:vercel

pause
