param([string]$zipPath)
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archiveTask=[IO.Compression.ZipFile]::OpenRead($zipPath)
try {
  $filesTask = @($archiveTask.Entries | Where-Object { -not $_.FullName.EndsWith('/') } | ForEach-Object {
    $relativeTask = ($_.FullName -split '/',2)[1]
    if ($relativeTask -and $relativeTask -notmatch '(^|/)(node_modules|\.git)(/|$)') {
      [pscustomobject]@{path=$relativeTask; bytes=$_.Length}
    }
  })
  ConvertTo-Json -InputObject $filesTask -Compress
} finally { $archiveTask.Dispose() }
