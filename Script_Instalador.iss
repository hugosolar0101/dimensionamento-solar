[Setup]
AppName=Dimensionamento Fotovoltaico
AppVersion=1.0
AppPublisher=Hugo Solar
DefaultDirName={autopf}\Dimensionamento Fotovoltaico
DefaultGroupName=Dimensionamento Fotovoltaico
OutputDir=Output
OutputBaseFilename=Instalador_Dimensionamento
Compression=lzma
SolidCompression=yes
SetupIconFile=icone.ico

[Languages]
Name: "portuguesebrazil"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
; Executável principal
Source: "dist\Teste.exe"; DestDir: "{app}"; Flags: ignoreversion

; Banco de dados (NÃO sobrescreve se já existir)
Source: "DIM2026.db"; DestDir: "{app}"; Flags: onlyifdoesntexist

; Controle de versão (pode atualizar)
Source: "versao.txt"; DestDir: "{app}"; Flags: ignoreversion

; Ícone (opcional)
Source: "icone.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Dimensionamento Fotovoltaico"; Filename: "{app}\Teste.exe"
Name: "{commondesktop}\Dimensionamento Fotovoltaico"; Filename: "{app}\Teste.exe"

[Run]
Filename: "{app}\Teste.exe"; Description: "Abrir o programa"; Flags: nowait postinstall skipifsilent