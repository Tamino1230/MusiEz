[Setup]
AppName=MusiEz - @tamino1230
AppVersion=1.0
DefaultDirName={pf}\MusiEz
DefaultGroupName=MusiEz
OutputBaseFilename=SetupMusiEz

[Files]
Source: "dist\main.exe"; DestDir: "{app}"

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,DeineApp}"; Flags: nowait postinstall skipifsilent
