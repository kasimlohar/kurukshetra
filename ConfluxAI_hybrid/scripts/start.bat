@echo off
echo Starting ConfluxAI Multi-Modal Search Agent Backend...
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "indexes" mkdir indexes
if not exist "logs" mkdir logs

REM Copy environment file if it doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo Created .env file from template
    )
)

echo.
echo ================================
echo ConfluxAI Backend Setup Complete
echo ================================
echo.
echo Starting the server...
echo API will be available at: http://localhost:8000
echo Documentation at: http://localhost:8000/docs
echo.

REM Start the FastAPI server
python main.py

pause
