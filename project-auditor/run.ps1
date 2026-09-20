param(
  [Parameter(Mandatory=$true)][string]$Path,
  [switch]$Run,
  [switch]$Install
)
$ArgsList = @("auditor.py", "--path", $Path, "--out", "audit-results")
if ($Run) { $ArgsList += "--run" }
if ($Install) { $ArgsList += "--install" }
python @ArgsList
