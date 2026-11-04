<#
.SYNOPSIS
  Build a diagnostic prompt request from programs_v11.yaml (prompt_defaults / scenarios).
.PARAMETER Scenario
  Named scenario from YAML (e.g. quick_brevet_entry).
.PARAMETER Set
  Extra KEY=VALUE overrides (array).
.PARAMETER Full
  Also write FULL.md = prompt file + request block.
.PARAMETER ListScenarios
  Print scenario names and exit.
.PARAMETER StdOut
  Print the request block to the console.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$PythonExe = '',
    [string]$Scenario = '',
    [string[]]$Set = @(),
    [switch]$Full,
    [switch]$ListScenarios,
    [switch]$StdOut
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')
$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo

$scriptArgs = @()
if ($ListScenarios) { $scriptArgs += '--list-scenarios' }
if ($Scenario) { $scriptArgs += @('--scenario', $Scenario) }
foreach ($s in $Set) { $scriptArgs += @('--set', $s) }
if ($Full) { $scriptArgs += '--full' }
if ($StdOut) { $scriptArgs += '--stdout' }

if ($WhatIfPreference) {
    Write-Host "Would run make_prompt_request_v11.py $($scriptArgs -join ' ')"
    $EnvInfo | Format-List
    return
}
$code = [int](Invoke-ProgramsPython -ScriptName 'make_prompt_request_v11.py' -ScriptArgs $scriptArgs -EnvInfo $EnvInfo -Isolated -LogName 'make_prompt_v11.log')
exit $code
