@echo off
setlocal

echo The window will close itself automaticly when its done!

:: path
set "CURRENT_DIR=%~dp0"

:: check if python is installed
echo check python
for %%i in (python.exe) do set "PYTHON_PATH=%%~$PATH:i"

if "%PYTHON_PATH%"=="" (
    echo Python is not installed. Getting installed...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo Python successfully installed.
) else (
    echo Python is already installed.
)

:: pip
echo installation of pip and python packages
python -m pip install --upgrade pip
python -m pip install yt-dlp pygame mutagen pypresence websockets flask flask-socketio werkzeug eventlet python-socketio matplotlib pywin32



echo Python-Packets successfully installed

:: check ffmpeg
echo Checking for ffmeg
if exist "%CURRENT_DIR%ffmpeg-7.1-essentials_build\bin\ffmpeg.exe" (
    echo ffmeg is already installed
) else (
    echo FFmpeg not found. installing...
    curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    tar -xf ffmpeg.zip
    del ffmpeg.zip
    echo FFmpeg successfully installed
)

set "folderpath=%~dp0"

set "desktop=%USERPROFILE%\Desktop"

set "shortcut=%desktop%\MusiEz - @tamino1230.lnk"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcut%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%folderpath%click and extract me.bat" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%folderpath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%folderpath%icon/babToma.ico" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"


cscript //nologo "%temp%\CreateShortcut.vbs"

del "%temp%\CreateShortcut.vbs"

echo Destopshortcut created

endlocal
