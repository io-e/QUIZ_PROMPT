<#
.SYNOPSIS
  Run validate_reference_v11.py against the referentiel and mirror reports to output/validation.
.PARAMETER PythonExe
  Optional full path to python.exe (otherwise YAML venv candidates, then py -3).
.PARAMETER WhatIf
  Show resolved paths without running.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$PythonExe = ''
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')

$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo

Write-Host "Validate reference package (structural only — not pedagogical approval)" -ForegroundColor Yellow
if ($WhatIfPreference) {
    $EnvInfo | Format-List | Out-String | Write-Host
    return
}
$code = [int](Invoke-ProgramsPython -ScriptName 'validate_reference_v11.py' -EnvInfo $EnvInfo -Isolated -LogName 'validate_reference_v11.log')
Copy-ValidationArtefacts -EnvInfo $EnvInfo -Config $Config
exit $code
