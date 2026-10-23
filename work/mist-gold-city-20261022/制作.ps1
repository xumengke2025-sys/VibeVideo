param([ValidateSet('layout','build','sample','full','assemble','score','verify')][string]$Mode='sample',[string]$Version='organic-final-v2')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython='C:\Users\67236\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$taskBlender=if($env:BLENDER){$env:BLENDER}else{'D:\ai项目\ai动画\VibeVideo项目\tools\blender-portable\blender-4.5.3-windows-x64\blender.exe'}
$env:FOG_VERSION=$Version
switch($Mode){
 'layout' { & $taskPython src/generate_layout.py }
 'build' { & $taskBlender --background --python-exit-code 1 --python src/build_world.py }
 'score' { & $taskPython src/compose_score.py }
 'verify' { & $taskPython src/verify_constraints.py }
 default { & $taskPython src/pipeline.py $Mode }
}
if($LASTEXITCODE -ne 0){throw "Production command exited with $LASTEXITCODE"}
