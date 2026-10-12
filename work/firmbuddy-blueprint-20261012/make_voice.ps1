$ErrorActionPreference = 'Stop'
$voiceRoot = Join-Path $PSScriptRoot 'audio'
$voice = New-Object -ComObject SAPI.SpVoice
$voice.Voice = $voice.GetVoices('Language=804').Item(0)
$voice.Rate = 1
$voice.Volume = 100
$texts = @(
'下午三点的客户拜访。',
'谈什么？依据在哪？下一步怎么做？',
'从商机中心找到值得研判的线索。',
'先看公告来源，再明确需要核实的问题。',
'企业画像、资本运作、信披合规。',
'多位专家围绕同一问题，补齐专业视角。',
'打开知识档案，查规则、找资料。',
'让分析连回来源与版本。',
'把客户情况、沟通重点和待核实问题，整理成拜访策略包。',
'再确认后续跟进任务。',
'从一条线索，到一次有准备的拜访。',
'<voice required="Language=409">Firm Buddy</voice><voice required="Language=804">，让专业协同，走进客户经营。</voice>'
)
for ($i=0; $i -lt $texts.Count; $i++) {
$voice.Rate = $(if($i -eq 1){3}else{1})
$stream = New-Object -ComObject SAPI.SpFileStream
$stream.Format.Type = 22
$voicePath = Join-Path $voiceRoot ('voice-{0:d2}.wav' -f $i)
$stream.Open($voicePath,3,$false)
$voice.AudioOutputStream = $stream
[void]$voice.Speak($texts[$i], $(if($i -eq 11){8}else{0}))
$stream.Close()
Write-Output "voice $i saved"
}
