param(
 [string]$NodeExe = 'node',
 [string]$PythonExe = 'python',
 [string]$Chrome = '',
 [string]$FFmpeg = 'ffmpeg',
 [string]$Playwright = '',
 [string[]]$Clips = @('blueprint-proof','dataviz-proof','one-way'),
 [string]$OutputRoot = 'out',
 [double]$Lufs = -18
)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
 & $NodeExe 'check.mjs'
 if ($LASTEXITCODE -ne 0) { throw 'Timeline check failed' }
 & $NodeExe 'test-contract.mjs'
 if ($LASTEXITCODE -ne 0) { throw 'Contract tests failed' }
 foreach ($clip in $Clips) {
  if ($clip -notmatch '^[a-z0-9-]+$') { throw 'Invalid clip name' }
  $taskOut = Join-Path $OutputRoot $clip
  $renderArgs = @('render.mjs',"--clip=$clip","--out=$taskOut","--ffmpeg=$FFmpeg")
  if ($Chrome) { $renderArgs += "--chrome=$Chrome" }
  if ($Playwright) { $renderArgs += "--playwright=$Playwright" }
  & $NodeExe @renderArgs
  if ($LASTEXITCODE -ne 0) { throw "Render failed: $clip" }
  & $PythonExe 'score.py' '--clip' $clip '--out' $taskOut '--ffmpeg' $FFmpeg '--lufs' $Lufs
  if ($LASTEXITCODE -ne 0) { throw "Sound build failed: $clip" }
 }
} finally { Pop-Location }
