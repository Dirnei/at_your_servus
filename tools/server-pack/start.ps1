# Servus server pack: installs NeoForge on first run, then starts the server. Needs Java 25.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$neoforge = '26.1.2.122'
if (-not (Test-Path 'run.bat')) {
    $installer = "neoforge-$neoforge-installer.jar"
    Invoke-WebRequest "https://maven.neoforged.net/releases/net/neoforged/neoforge/$neoforge/$installer" -OutFile $installer
    & java -jar $installer --installServer
    if ($LASTEXITCODE -ne 0) { throw 'NeoForge installer failed' }
    Remove-Item $installer, "$installer.log" -ErrorAction SilentlyContinue
}
if (-not ((Test-Path 'eula.txt') -and (Select-String -Path 'eula.txt' -Pattern 'eula=true' -Quiet))) {
    Write-Host 'Read https://aka.ms/MinecraftEULA and set eula=true in eula.txt, then start again.'
    Set-Content 'eula.txt' 'eula=false'
    exit 1
}
& .\run.bat nogui
