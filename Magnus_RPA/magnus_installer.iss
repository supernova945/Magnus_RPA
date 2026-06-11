[Setup]
; Identificador único de tu aplicación
AppId={{DAA3D0B9-9F81-4C10-B8B7-7A2B09F7C4B2}}
AppName=Magnus
AppVersion=1.0.0
AppPublisher=Franco Paolo López Gálvez
AppPublisherURL=https://www.crediopciones.com/
AppSupportURL=https://www.crediopciones.com/
AppUpdatesURL=https://www.crediopciones.com/
; Instalación local sin privilegios
PrivilegesRequired=lowest
DefaultDirName={autopf}\Magnus
DefaultGroupName=Magnus
AllowNoIcons=yes
; Icono del instalador
SetupIconFile=recursos\magnus.ico
OutputDir=.
OutputBaseFilename=Instalador_Magnus
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copia el ejecutable principal y el icono para que esté disponible en la carpeta de instalación
Source: "dist\Magnus.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "recursos\magnus.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Se especifica IconFilename para asegurar que el sistema encuentre el icono correctamente
Name: "{group}\Magnus"; Filename: "{app}\Magnus.exe"; IconFilename: "{app}\magnus.ico"
Name: "{autodesktop}\Magnus"; Filename: "{app}\Magnus.exe"; Tasks: desktopicon; IconFilename: "{app}\magnus.ico"

[Run]
Filename: "{app}\Magnus.exe"; Description: "{cm:LaunchProgram,Magnus}"; Flags: nowait postinstall skipifsilent