$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$archiveRoot = Join-Path $taskRoot '_archive/versions-before-v17-20261022'
if (Test-Path -LiteralPath $archiveRoot) { throw 'Archive already exists; inspect before repeating.' }
$protected = @{}
foreach ($version in @(17,18)) {
    $manifest = Get-Content -LiteralPath (Join-Path $taskRoot "out/source-runtime-v$version/SOURCE-PACKAGE.json") -Raw | ConvertFrom-Json
    foreach ($property in $manifest.sha256.PSObject.Properties) { $protected[$property.Name] = $true }
}
$candidates = [Collections.Generic.List[object]]::new()
foreach ($file in Get-ChildItem -LiteralPath (Join-Path $taskRoot 'out') -File) {
    if ($file.Extension -notin @('.mp4','.zip')) { continue }
    if ($file.Name -match '^mother-baby-(20-eras-portrait-v(17|18)-40s\.mp4|v(17|18)-source-and-assets\.zip)$') { continue }
    $candidates.Add($file)
}
foreach ($folder in @('', 'film')) {
    $directory = if ($folder) { Join-Path $taskRoot $folder } else { $taskRoot }
    foreach ($file in Get-ChildItem -LiteralPath $directory -File) {
        if ($file.Extension -notin @('.py','.mjs','.js','.html')) { continue }
        if ($file.Name -notmatch 'v(\d+)') { continue }
        if ([int]$Matches[1] -ge 17) { continue }
        $relative = $file.FullName.Substring($taskRoot.Length+1).Replace('\','/')
        if (-not $protected.ContainsKey($relative)) { $candidates.Add($file) }
    }
}
foreach ($directory in Get-ChildItem -LiteralPath (Join-Path $taskRoot 'out') -Directory) {
    if ($directory.Name -match '^source-runtime-v(\d+)$' -and [int]$Matches[1] -lt 17) { $candidates.Add($directory) }
}
$records = @()
foreach ($item in $candidates) {
    $source = [IO.Path]::GetFullPath($item.FullName)
    $relative = $source.Substring($taskRoot.Length+1)
    $target = [IO.Path]::GetFullPath((Join-Path $archiveRoot $relative))
    if (-not $source.StartsWith($taskRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or -not $target.StartsWith($archiveRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw "Unsafe path: $source" }
    if ($protected.ContainsKey($relative.Replace('\','/'))) { throw "Protected: $relative" }
    $bytes = if ($item.PSIsContainer) { (Get-ChildItem -LiteralPath $source -File -Recurse | Measure-Object Length -Sum).Sum } else { $item.Length }
    $records += [pscustomobject]@{source=$source;target=$target;relative=$relative;directory=$item.PSIsContainer;bytes=$bytes}
}
New-Item -ItemType Directory -Path $archiveRoot | Out-Null
$records | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $archiveRoot 'restore-manifest.json') -Encoding utf8
foreach ($record in $records) {
    $parent = Split-Path -Parent $record.target
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    Move-Item -LiteralPath $record.source -Destination $record.target
}
foreach ($relative in $protected.Keys) {
    if (-not (Test-Path -LiteralPath (Join-Path $taskRoot $relative) -PathType Leaf)) { throw "Missing retained dependency: $relative" }
}
[pscustomobject]@{archived_items=$records.Count;archived_bytes=($records | Measure-Object bytes -Sum).Sum;retained_manifest_files=$protected.Count;permanently_deleted=0;archive=$archiveRoot} | ConvertTo-Json | Tee-Object -FilePath (Join-Path $archiveRoot 'result.json')
