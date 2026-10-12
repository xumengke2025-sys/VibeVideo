$ErrorActionPreference = 'Stop'
$base = 'D:\ai项目\ai动画'
$target = Join-Path $base 'VibeVideo项目'
$records = [System.Collections.Generic.List[object]]::new()
function Inventory([string]$root) {
  @(Get-ChildItem -LiteralPath $root -File -Recurse | Where-Object { $_.FullName -notmatch '\\(node_modules|\.git)\\' } | ForEach-Object {
    [pscustomobject]@{path=$_.FullName.Substring($root.Length).TrimStart('\'); bytes=$_.Length; sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
  })
}
function Verify([string]$root, $items) {
  foreach ($item in $items) {
    $file = Join-Path $root $item.path
    if (!(Test-Path -LiteralPath $file) -or (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $item.sha256) { throw "Verification failed: $file" }
  }
}
$names = @('black-hole-lensing-20261008','director-study-20261008','light-to-lens-20261008','morpho-blue-20261008','reference-study-20261008','skill-refinement-20261007','vibe-video-proof')
New-Item -ItemType Directory -Path (Join-Path $target 'work') -Force | Out-Null
foreach ($name in $names) {
  $src = [IO.Path]::GetFullPath((Join-Path "$base\work" $name))
  $dst = [IO.Path]::GetFullPath((Join-Path "$target\work" $name))
  if (!$src.StartsWith("$base\work\") -or !$dst.StartsWith("$target\work\")) { throw 'Invalid containment' }
  if (Test-Path -LiteralPath $dst) { throw "Destination exists: $dst" }
  $items = Inventory $src
  Move-Item -LiteralPath $src -Destination $dst
  New-Item -ItemType Junction -Path $src -Target $dst | Out-Null
  Verify $dst $items
  $records.Add([pscustomobject]@{action='move-with-compatibility-junction';source=$src;destination=$dst;files=$items})
  Write-Output "Moved and verified: $name ($($items.Count) files)"
}
$copies = @(
  @('C:\CodexTemp\vibe-reference-media-20261008', 'reference-sources\bilibili-media'),
  @('C:\CodexTemp\pdoom-review-20261008', 'reference-sources\pdoom-source-review'),
  @('D:\Codex\skills\vibe-video', 'skill\vibe-video')
)
foreach ($pair in $copies) {
  $src = $pair[0]; $dst = Join-Path $target $pair[1]
  $items = Inventory $src
  foreach ($item in $items) {
    $file = Join-Path $dst $item.path
    New-Item -ItemType Directory -Path (Split-Path $file) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $src $item.path) -Destination $file
  }
  Verify $dst $items
  $records.Add([pscustomobject]@{action='snapshot-copy';source=$src;destination=$dst;files=$items})
  Write-Output "Copied and verified: $($pair[1]) ($($items.Count) files)"
}
Copy-Item -LiteralPath 'C:\Users\67236\.codex\attachments\82b95ba1-ad2e-4e3e-81f0-a7cbdf1f4b00\goal-objective.md' -Destination "$target\goal-objective.md"
foreach ($name in @('package.json','package-lock.json')) {
  if (Test-Path -LiteralPath "$base\$name") { Copy-Item -LiteralPath "$base\$name" -Destination "$target\runtime-$name" }
}
New-Item -ItemType Junction -Path "$target\node_modules" -Target "$base\node_modules" | Out-Null
[pscustomobject]@{created=(Get-Date -Format o);verified='SHA256 for every moved/copied project file';entries=$records} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath "$target\organization-manifest.json" -Encoding utf8
Write-Output 'Organization complete.'
