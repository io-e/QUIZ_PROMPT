<#
.SYNOPSIS
  Build the static HTML demonstration quiz (NOT a validated student assessment).
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param([string]$PythonExe = '')
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')
$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo
Write-Host "Demo quiz only — UNVALIDATED prototype" -ForegroundColor Yellow
if ($WhatIfPreference) { $EnvInfo | Format-List; return }
$code = [int](Invoke-ProgramsPython -ScriptName 'make_demo_quiz_html.py' -EnvInfo $EnvInfo -Isolated -LogName 'demo_quiz_v11.log')
exit $code
