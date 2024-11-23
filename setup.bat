@echo off
setlocal

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
"%PYTHON_PATH%" -m pip install --upgrade pip
"%PYTHON_PATH%" -m pip install yt-dlp
"%PYTHON_PATH%" -m pip install pygame
"%PYTHON_PATH%" -m pip install mutagen
"%PYTHON_PATH%" -m pip install pypresence

echo Python packages installed successfully.

:: Check if ffmpeg is installed
echo Checking for FFmpeg installation...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo FFmpeg is not installed. Downloading and installing FFmpeg...
    curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    tar -xf ffmpeg.zip -C %cd%
    setx PATH "%cd%\ffmpeg\bin;%PATH%"
    del ffmpeg.zip
    echo FFmpeg installed successfully.
) else (
    echo FFmpeg is already installed.
)

endlocal
