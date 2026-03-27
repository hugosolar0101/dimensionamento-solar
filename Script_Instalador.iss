[Setup]
AppName=Dimensionamento Fotovoltaico
AppVersion=1.0
DefaultDirName={pf}\Dimensionamento Fotovoltaico
DefaultGroupName=Dimensionamento Fotovoltaico
OutputDir=.
OutputBaseFilename=Instalador_Dimensionamento
SetupIconFile=icone.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Teste.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "DIM2026.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "icone.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Dimensionamento Fotovoltaico"; Filename: "{app}\Teste.exe"
Name: "{commondesktop}\Dimensionamento Fotovoltaico"; Filename: "{app}\Teste.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Opções adicionais:"