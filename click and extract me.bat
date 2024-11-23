@echo off
echo Searching for Python...
for %%i in (python.exe) do set "PYTHON_PATH=%%~$PATH:i"

REM Finding...
if "%PYTHON_PATH%"=="" (
    echo python is not installed. Please Open setup.bat first.
    exit /b 1
)

echo looking for path...
set "SCRIPT_DIR=%~dp0"

echo start...
cd /d "%SCRIPT_DIR%"
"%PYTHON_PATH%" "%SCRIPT_DIR%main.py"
pause
