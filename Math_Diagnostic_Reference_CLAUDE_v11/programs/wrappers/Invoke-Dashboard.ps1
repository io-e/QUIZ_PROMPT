<#
.SYNOPSIS
  Generate validation_dashboard_v11.html from the last validation reports.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param([string]$PythonExe = '')
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')
$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo
if ($WhatIfPreference) { $EnvInfo | Format-List; return }
$code = [int](Invoke-ProgramsPython -ScriptName 'v11_html_dashboard.py' -EnvInfo $EnvInfo -Isolated -LogName 'dashboard_v11.log')
Copy-ValidationArtefacts -EnvInfo $EnvInfo -Config $Config
exit $code
