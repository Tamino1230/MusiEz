@echo off
setlocal

echo The window will close itself automatically when it's done!

:: path
set "CURRENT_DIR=%~dp0"

:: check if python is installed
echo Checking for Python...
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

:: create executable from main.py
echo Converting main.py to main.exe...
pyinstaller --onefile main.py

:: move folder
echo Moving folder...
set "source_folder=%~dp0"
set "target_folder=C:\Path\to\MainFolder"

xcopy /E /I "%source_folder%" "%target_folder%\MusiEz - @tamino1230"

:: create desktop shortcut
set "folderpath=%~dp0"
set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\MusiEz - @tamino1230.lnk"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcut%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%folderpath%dist\main.exe" >> "%temp%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%folderpath%" >> "%temp%\CreateShortcut.vbs"
echo oLink.IconLocation = "%folderpath%icon/babToma.ico" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

cscript //nologo "%temp%\CreateShortcut.vbs"
del "%temp%\CreateShortcut.vbs"

:: cleanup
echo Cleaning up...
rmdir /s /q build
del main.spec
echo Done!
pause
endlocal
