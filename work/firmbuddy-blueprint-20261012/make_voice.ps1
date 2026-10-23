$ErrorActionPreference = 'Stop'
$voiceRoot = Join-Path $PSScriptRoot 'audio'
$voice = New-Object -ComObject SAPI.SpVoice
$voice.Voice = $voice.GetVoices('Language=804').Item(0)
$voice.Rate = 1
$voice.Volume = 100
$entries = Get-Content -LiteralPath (Join-Path $voiceRoot 'script-v3.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$texts = @($entries | ForEach-Object { [string]$_[2] })
for ($i=0; $i -lt $texts.Count; $i++) {
$voice.Rate = 2
if($i -eq 1){$voice.Rate = 4}
$texts[$i] = $texts[$i].Replace('Firm Buddy','<voice required="Language=409">Firm Buddy</voice><voice required="Language=804"></voice>')
$stream = New-Object -ComObject SAPI.SpFileStream
$stream.Format.Type = 22
$voicePath = Join-Path $voiceRoot ('voice-{0:d2}.wav' -f $i)
$stream.Open($voicePath,3,$false)
$voice.AudioOutputStream = $stream
[void]$voice.Speak($texts[$i], 8)
$stream.Close()
Write-Output "voice $i saved"
}
