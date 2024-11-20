@echo off
setlocal

REM Check if any files are dropped onto the batch file
if "%~1"=="" (
    echo No files dropped. Please drag and drop one or more .yml files onto this script.
    pause
    exit /b
)

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed or not found on the system. Please install Docker and try again.
    pause
    exit /b
)

REM Loop through each dropped file and run docker-compose up
for %%F in (%*) do (
    start cmd /k "docker-compose -f "%%~F" up --build"
)

:end