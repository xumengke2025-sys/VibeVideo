param(
    [ValidateSet('plan','status','build','build-proof','proof','sample','full')]
    [string]$Mode = 'plan',
    [string]$Version = 'film-v2',
    [ValidateRange(1,48)][int]$BatchSize = 24,
    [ValidateRange(1,4096)][int]$Samples = 32,
    [ValidateSet('CYCLES','EEVEE')][string]$Engine = 'CYCLES',
    [int[]]$Frames
)
$ErrorActionPreference = 'Stop'
$filmRoot = $PSScriptRoot
$projectRoot = Split-Path (Split-Path $filmRoot -Parent) -Parent
$filmPython = Join-Path $projectRoot 'tools\blender-portable\blender-4.5.3-windows-x64\4.5\python\bin\python.exe'
$filmEntry = Join-Path $filmRoot 'src\film_pipeline.py'
$filmArguments = @('-X','utf8',$filmEntry,$Mode,'--version',$Version,'--batch-size',"$BatchSize",'--samples',"$Samples",'--engine',$Engine)
if ($PSBoundParameters.ContainsKey('Frames')) { $filmArguments += '--frames'; $filmArguments += $Frames | ForEach-Object { "$_" } }
& $filmPython @filmArguments
if ($LASTEXITCODE -ne 0) { throw "Film pipeline failed with exit code $LASTEXITCODE. Inspect version status and logs before resuming." }
