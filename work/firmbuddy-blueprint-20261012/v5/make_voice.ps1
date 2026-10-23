$ErrorActionPreference = 'Stop'
$voiceRoot = Join-Path $PSScriptRoot 'audio'
$voice = New-Object -ComObject SAPI.SpVoice
$voice.Voice = $voice.GetVoices('Language=804').Item(0)
$voice.Rate = 2
$voice.Volume = 100
$entries = (Get-Content -LiteralPath (Join-Path $PSScriptRoot 'plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json).shots
for ($i=0; $i -lt $entries.Count; $i++) {
  $voice.Rate = 2
  if ($i -eq 0 -or $i -eq 6) { $voice.Rate = 2 }
  if ([string]::IsNullOrWhiteSpace($entries[$i].voiceover)) { continue }
  $voicePath = Join-Path $voiceRoot ('voice-{0:d2}.wav' -f $i)
  $stream = New-Object -ComObject SAPI.SpFileStream
  $stream.Format.Type = 22
  $stream.Open($voicePath,3,$false)
  $voice.AudioOutputStream = $stream
  $spoken = ([string]$entries[$i].voiceover).Replace('AI','人工智能')
  [void]$voice.Speak($spoken, 0)
  $stream.Close()
  Write-Output "voice $i saved"
}
