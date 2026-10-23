param([Parameter(Mandatory=$true)][int]$TaskProcessId,[Parameter(Mandatory=$true)][string]$ExpectedCommand)
$taskProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $TaskProcessId"
if (!$taskProcess -or !$taskProcess.CommandLine.Contains($ExpectedCommand)) { throw 'Process identity mismatch' }
$taskProcesses = @(Get-CimInstance Win32_Process)
function Stop-TaskChildren([int]$parent) {
    foreach ($child in $taskProcesses | Where-Object ParentProcessId -eq $parent) {
        Stop-TaskChildren $child.ProcessId
        Stop-Process -Id $child.ProcessId -ErrorAction SilentlyContinue
    }
}
Stop-TaskChildren $TaskProcessId
Stop-Process -Id $TaskProcessId -ErrorAction SilentlyContinue
