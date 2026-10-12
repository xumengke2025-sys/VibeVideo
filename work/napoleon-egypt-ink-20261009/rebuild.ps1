$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$videoNode = 'D:/docker/node.exe'
$videoPython = 'C:/Users/67236/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$videoFfmpeg = 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe'
$videoOutput = 'out/rebuild-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
& $videoNode render.mjs "--out=$videoOutput"
if ($LASTEXITCODE -ne 0) { throw 'Picture render failed' }
& $videoPython -X utf8 score.py
if ($LASTEXITCODE -ne 0) { throw 'Audio render failed' }
& $videoFfmpeg -hide_banner -loglevel error -y -i "$videoOutput/picture.mp4" -i 'out/score.wav' -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -af 'loudnorm=I=-20:TP=-1.5:LRA=12' -ar 48000 -t 60 -movflags +faststart "$videoOutput/napoleon-egypt-ink.mp4"
if ($LASTEXITCODE -ne 0) { throw 'Final mux failed' }
Write-Output "$PSScriptRoot/$videoOutput/napoleon-egypt-ink.mp4"
