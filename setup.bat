@echo off
setlocal

:: Pfad des aktuellen Skripts abrufen
set "CURRENT_DIR=%~dp0"

:: Check if Python is installed
echo Checking for Python installation...
for %%i in (python.exe) do set "PYTHON_PATH=%%~$PATH:i"

if "%PYTHON_PATH%"=="" (
    echo Python is not installed. Downloading and installing Python...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python installed successfully.
) else (
    echo Python is already installed.
)

:: Upgrade pip and install required Python packages
echo Installing Python packages...
python -m pip install --upgrade pip
python -m pip install yt-dlp pygame mutagen pypresence

echo Python packages installed successfully.

:: Check if ffmpeg is in the same directory as the script
echo Checking for FFmpeg installation in the script directory...
if exist "%CURRENT_DIR%ffmpeg.exe" (
    echo FFmpeg is already in the script directory.
) else (
    echo FFmpeg is not found in the script directory. Downloading and installing FFmpeg...
    curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    tar -xf ffmpeg.zip
    del ffmpeg.zip
    echo FFmpeg installed successfully in the script directory.
)

endlocal
