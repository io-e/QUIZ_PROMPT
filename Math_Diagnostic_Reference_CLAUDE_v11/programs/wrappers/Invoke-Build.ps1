<#
.SYNOPSIS
  Run build_v11.py. Default is --check (read-only). Pass -Apply to write files.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$PythonExe = '',
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')
$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo
$scriptArgs = @()
if (-not $Apply) { $scriptArgs += '--check' }
if ($WhatIfPreference) { Write-Host "Would run build_v11.py $($scriptArgs -join ' ')"; $EnvInfo | Format-List; return }
if ($Apply -and -not $PSCmdlet.ShouldProcess($EnvInfo.Referentiel, 'Write v11 build outputs')) { exit 1 }
$code = [int](Invoke-ProgramsPython -ScriptName 'build_v11.py' -ScriptArgs $scriptArgs -EnvInfo $EnvInfo -Isolated -LogName 'build_v11.log')
exit $code
