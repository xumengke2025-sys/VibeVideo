$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskBlender=if($env:BLENDER){$env:BLENDER}else{'D:\ai项目\ai动画\VibeVideo项目\tools\blender-portable\blender-4.5.3-windows-x64\blender.exe'}
& $taskBlender --python src/open_editable.py
