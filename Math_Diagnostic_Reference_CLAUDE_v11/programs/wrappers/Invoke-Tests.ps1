<#
.SYNOPSIS
  Run tests_v11.py (eligibility / release-logic regression suite).
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param([string]$PythonExe = '')
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')
$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo
if ($WhatIfPreference) { $EnvInfo | Format-List; return }
$code = [int](Invoke-ProgramsPython -ScriptName 'tests_v11.py' -EnvInfo $EnvInfo -Isolated -LogName 'tests_v11.log')
exit $code
