# Installs the client side of the working tree into a dev CurseForge profile, for testing on the local server
# without building and importing the client zip. Only changed files are downloaded; files the pack dropped are removed.
#   .\tools\client-sync.ps1                       syncs into the profile "At Your Servus (dev)"
#   -Instance <folder>                            another profile folder
# Needs packwiz and Java on PATH. Runs on Windows PowerShell 5.1 and PowerShell 7.
param([string]$Instance = (Join-Path $env:USERPROFILE 'curseforge\minecraft\Instances\At Your Servus (dev)'))
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$bootstrap = Join-Path $root 'build/tools/packwiz-installer-bootstrap.jar'
$port = 28418
$bootstrapUrl = 'https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar'

if (-not (Test-Path $Instance)) {
    throw "No profile at $Instance. In the CurseForge app: Create Custom Profile, name it 'At Your Servus (dev)', Minecraft 26.1.2, NeoForge 26.1.2.122, then run this again."
}

# The CurseForge app installs Minecraft and NeoForge; a profile on other versions cannot load the pack.
$packToml = [IO.File]::ReadAllText((Join-Path $root 'pack.toml'))
$minecraft = [regex]::Match($packToml, '(?m)^minecraft = "(.*)"$').Groups[1].Value
$neoforge = [regex]::Match($packToml, '(?m)^neoforge = "(.*)"$').Groups[1].Value
$instanceJson = Join-Path $Instance 'minecraftinstance.json'
if (Test-Path $instanceJson) {
    $cfProfile = Get-Content $instanceJson -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($cfProfile.gameVersion -ne $minecraft -or $cfProfile.baseModLoader.name -ne "neoforge-$neoforge") {
        Write-Warning "The profile has Minecraft $($cfProfile.gameVersion) with $($cfProfile.baseModLoader.name), the pack needs $minecraft with neoforge-$neoforge"
    }
}

Push-Location $root
try {
    & packwiz refresh
    if ($LASTEXITCODE -ne 0) { throw "packwiz refresh failed (exit $LASTEXITCODE)" }
    if (-not (Test-Path $bootstrap)) {
        New-Item -ItemType Directory -Force (Split-Path $bootstrap) | Out-Null
        Invoke-WebRequest $bootstrapUrl -OutFile $bootstrap
    }
    $serve = Start-Process packwiz -ArgumentList 'serve', '--port', "$port" -PassThru -NoNewWindow
    try {
        $ready = $false
        for ($i = 0; $i -lt 60 -and -not $ready; $i++) {
            try { Invoke-WebRequest "http://localhost:$port/pack.toml" -UseBasicParsing | Out-Null; $ready = $true }
            catch { Start-Sleep -Milliseconds 500 }
        }
        if (-not $ready) { throw 'packwiz serve did not start' }
        Push-Location $Instance
        try {
            # Windows PowerShell 5.1 turns native stderr into errors under 'Stop'.
            $ErrorActionPreference = 'Continue'
            & java -jar $bootstrap -g -s client "http://localhost:$port/pack.toml" 2>&1 | ForEach-Object { "$_" } | Write-Host
            $exit = $LASTEXITCODE
            $ErrorActionPreference = 'Stop'
            if ($exit -ne 0) { throw "packwiz-installer failed (exit $exit)" }
        } finally { Pop-Location }
    } finally {
        Stop-Process -Id $serve.Id -ErrorAction SilentlyContinue
    }
    Write-Host "Synced $Instance; start the profile in the CurseForge app and join localhost:25567"
} finally {
    Pop-Location
}
