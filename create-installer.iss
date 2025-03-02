#define MyAppName "Auto Commit với Copilot"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Your Name"
#define MyAppURL "https://github.com/yourusername/auto-commit-copilot"
#define MyAppExeName "Auto-Commit-Installer.exe"
#define VSCodeExtensionsDir "{code:GetVSCodeExtensionsDir}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{E8F3AC9D-7C2F-4F8A-B7E9-3F2E0A8F3D5C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=Auto-Commit-Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "extension\auto-commit-copilot-0.0.1.vsix"; DestDir: "{app}"; Flags: ignoreversion
Source: "extension\*"; DestDir: "{app}\extension"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "install-extension.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\install-extension.bat"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\install-extension.bat"; Tasks: desktopicon

[Run]
Filename: "{app}\install-extension.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function GetVSCodeExtensionsDir(Param: string): string;
var
  VSCodeExtDir: string;
begin
  VSCodeExtDir := ExpandConstant('{userappdata}') + '\Code\User\extensions';
  if DirExists(VSCodeExtDir) then
    Result := VSCodeExtDir
  else
    Result := ExpandConstant('{app}');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Tạo file bat để cài đặt extension
    SaveStringToFile(ExpandConstant('{app}\install-extension.bat'),
      '@echo off' + #13#10 +
      'echo Installing Auto Commit with Copilot extension...' + #13#10 +
      'code --install-extension "' + ExpandConstant('{app}') + '\auto-commit-copilot-0.0.1.vsix"' + #13#10 +
      'echo Installation completed. Please restart VS Code if it is running.' + #13#10 +
      'pause', False);
  end;
end; 