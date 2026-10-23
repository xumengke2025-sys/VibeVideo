$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
$taskCues = Get-Content -LiteralPath (Join-Path $taskRoot 'film/narration.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskVoice = New-Object -ComObject SAPI.SpVoice
$taskVoice.Voice = $taskVoice.GetVoices() | Where-Object { $_.GetDescription() -like '*Huihui*' } | Select-Object -First 1
$taskVoice.Rate = 1
$taskVoice.Volume = 100
$taskIndex = 0
foreach ($taskCue in $taskCues) {
    $taskName = '{0:D2}.wav' -f $taskIndex
    $taskPath = Join-Path $taskRoot ('film/narration/' + $taskName)
    $taskStream = New-Object -ComObject SAPI.SpFileStream
    $taskStream.Format.Type = 22
    $taskStream.Open($taskPath, 3, $false)
    $taskVoice.AudioOutputStream = $taskStream
    $null = $taskVoice.Speak($taskCue.text)
    $taskStream.Close()
    $taskDuration = & 'D:/ai项目/ai动画/node_modules/@remotion/compositor-win32-x64-msvc/ffprobe.exe' -v error -show_entries format=duration -of default=nw=1:nk=1 $taskPath
    $taskCue | Add-Member -NotePropertyName duration -NotePropertyValue ([double]$taskDuration) -Force
    $taskCue | Add-Member -NotePropertyName file -NotePropertyValue ('narration/' + $taskName) -Force
    $taskCue | Add-Member -NotePropertyName voice -NotePropertyValue 'Microsoft Huihui Desktop' -Force
    $taskCue | Add-Member -NotePropertyName synthetic -NotePropertyValue $true -Force
    Write-Output ($taskCue.id + ': ' + $taskDuration + 's')
    $taskIndex++
}
$taskCues | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot 'film/narration.json') -Encoding UTF8
