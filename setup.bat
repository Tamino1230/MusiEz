@echo off
setlocal

echo The window will close itself automatically when it's done!

:: path
set "CURRENT_DIR=%~dp0"

:: check if python is installed
echo Checking for Python...
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed. Please Install it manually
    exit
) else (
    echo Python is already installed.
)

:: pip
echo Installing pip and Python packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo Python packages successfully installed.

:: check ffmpeg
echo Checking for FFmpeg...
if exist "%CURRENT_DIR%ffmpeg-7.1-essentials_build\bin\ffmpeg.exe" (
    echo FFmpeg is already installed.
) else (
    echo FFmpeg not found. Installing...
    curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    tar -xf ffmpeg.zip
    del ffmpeg.zip
    echo FFmpeg successfully installed.
)

set "folderpath=%~dp0"
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\babTomaMusic - @tamino1230.lnk"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcut%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%folderpath%main.exe" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%folderpath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%folderpath%icon/babToma.ico" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

cscript //nologo "%temp%\CreateShortcut.vbs"
del "%temp%\CreateShortcut.vbs"

echo Done!
endlocal
echo .
echo Have fun!
