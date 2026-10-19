# Builds the Servus pack into dist/: the CurseForge client zip and the server pack.
#   .\tools\build.ps1           playtest build (mods from GitHub ride along in the client zip)
#   .\tools\build.ps1 -Public   public build, fails if any mod is not from CurseForge
#   -Version 0.1.0-alpha        version for the zips and the manifest (default dev); pack.toml keeps "dev",
#                               the release tag is the only place the version is written
# Needs packwiz, Java and Python on PATH. Runs on Windows PowerShell 5.1 and PowerShell 7.
param([switch]$Public, [string]$Version = 'dev')
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$dist = Join-Path $root 'dist'
$build = Join-Path $root 'build'
$server = Join-Path $build 'server'
$bootstrap = Join-Path $build 'tools/packwiz-installer-bootstrap.jar'
$port = 28417
$bootstrapUrl = 'https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar'

function Invoke-Step([string]$what, [scriptblock]$block) {
    Write-Host "== $what"
    & $block
    if ($LASTEXITCODE -ne 0) { throw "$what failed (exit $LASTEXITCODE)" }
}

Push-Location $root
$packToml = [IO.File]::ReadAllText((Join-Path $root 'pack.toml'))
try {
    # The version only exists for this build; pack.toml is restored in finally.
    $version = $Version
    [IO.File]::WriteAllText((Join-Path $root 'pack.toml'), ($packToml -replace '(?m)^version = ".*"$', "version = `"$version`""))
    $client = Join-Path $dist "at-your-servus-$version.zip"
    $serverZip = Join-Path $dist "at-your-servus-$version-server.zip"

    $checkArgs = @('-m', 'tools.checks.pack_check')
    if ($Public) { $checkArgs += '--public' }
    Invoke-Step 'pack check' { & python @checkArgs }
    Invoke-Step 'quest generator' { & python -m tools.questgen.generate }
    Invoke-Step 'packwiz refresh' { & packwiz refresh }

    New-Item -ItemType Directory -Force $dist | Out-Null
    Remove-Item $client, $serverZip -ErrorAction SilentlyContinue
    Invoke-Step 'client pack' { & packwiz curseforge export -o $client }
    Invoke-Step 'profile image' { & python -m tools.ziptool image $client art/logo/at-your-servus-square-8x.png }

    # Server pack: packwiz-installer installs the server side of the pack from a local packwiz serve.
    if (-not (Test-Path $bootstrap)) {
        New-Item -ItemType Directory -Force (Split-Path $bootstrap) | Out-Null
        Invoke-WebRequest $bootstrapUrl -OutFile $bootstrap
    }
    if (Test-Path $server) { Remove-Item -Recurse -Force $server }
    New-Item -ItemType Directory -Force $server | Out-Null
    $serve = Start-Process packwiz -ArgumentList 'serve', '--port', "$port" -PassThru -NoNewWindow
    try {
        $ready = $false
        for ($i = 0; $i -lt 60 -and -not $ready; $i++) {
            try { Invoke-WebRequest "http://localhost:$port/pack.toml" -UseBasicParsing | Out-Null; $ready = $true }
            catch { Start-Sleep -Milliseconds 500 }
        }
        if (-not $ready) { throw 'packwiz serve did not start' }
        Push-Location $server
        try {
            # Windows PowerShell 5.1 turns native stderr into errors under 'Stop'.
            $ErrorActionPreference = 'Continue'
            $log = & java -jar $bootstrap -g -s server "http://localhost:$port/pack.toml" 2>&1
            $exit = $LASTEXITCODE
            $ErrorActionPreference = 'Stop'
            $log | ForEach-Object { "$_" } | Write-Host
        } finally { Pop-Location }
        $failed = $log | ForEach-Object { "$_" } | Where-Object { $_ -match 'Failed to download [^m]|must be downloaded manually|^Please go to' } | Select-Object -Unique
        if ($exit -ne 0 -or $failed) {
            throw "server pack: some files could not be downloaded:`n$($failed -join "`n")"
        }
    } finally {
        Stop-Process -Id $serve.Id -ErrorAction SilentlyContinue
    }
    if (-not (Test-Path (Join-Path $server 'config/ftbquests/quests/data.json5'))) { throw 'server pack: the quest book is missing (check .packwizignore)' }
    Copy-Item (Join-Path $root 'tools/server-pack/start.sh'), (Join-Path $root 'tools/server-pack/start.ps1') $server
    Invoke-Step 'server zip' { & python -m tools.ziptool dir $server $serverZip --exclude packwiz.json --exclude packwiz-installer.jar }
    Copy-Item $serverZip (Join-Path $dist 'at-your-servus-latest-server.zip') -Force

    # Mods that are not on CurseForge cannot be in the manifest; packwiz export puts them in overrides/mods.
    foreach ($jar in (& python -m tools.checks.pack_check --list-url-mods)) {
        Write-Warning "$jar is not from CurseForge: $(Split-Path -Leaf $client) is a playtest pack, not for public upload"
    }

    # The quest check needs the server pack's jars to know every item ID.
    Invoke-Step 'quest check' { & python -m tools.checks.quest_check --mods (Join-Path $server 'mods') }
    Invoke-Step 'script check' { & python -m tools.checks.script_check --mods (Join-Path $server 'mods') }
    Invoke-Step 'version check' { & python -m tools.checks.version_check --client-zip $client --server-mods (Join-Path $server 'mods') }
    Write-Host "Built $client and $serverZip"
} finally {
    [IO.File]::WriteAllText((Join-Path $root 'pack.toml'), $packToml)
    Pop-Location
}
