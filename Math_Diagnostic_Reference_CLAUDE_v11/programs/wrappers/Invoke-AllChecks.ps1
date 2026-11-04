<#
.SYNOPSIS
  Run the full technical kit: tests → build --check → validate → dashboard.
  Same intent as RUN_TESTS_V11.cmd, using YAML paths and output mirroring.
.PARAMETER ContinueOnBuildDiff
  If build_v11.py --check exits non-zero (common on Windows when packaged
  files use CRLF and the builder writes LF), warn and continue with validate
  and dashboard instead of aborting the kit.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$PythonExe = '',
    [switch]$ContinueOnBuildDiff
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\lib\Common.ps1')
$Config = Import-ProgramsConfig -PythonExe $PythonExe
$EnvInfo = Initialize-ProgramsEnvironment -Config $Config -PythonExe $PythonExe
Test-ProgramsPrerequisites -EnvInfo $EnvInfo

Write-Host "=== [1/4] Regression tests ===" -ForegroundColor Cyan
$code = [int](Invoke-ProgramsPython -ScriptName 'tests_v11.py' -EnvInfo $EnvInfo -Isolated -LogName 'tests_v11.log')
if ($code -ne 0) { Write-Error "tests_v11.py failed (exit $code)"; exit $code }

Write-Host "=== [2/4] Build check (read-only) ===" -ForegroundColor Cyan
$code = [int](Invoke-ProgramsPython -ScriptName 'build_v11.py' -ScriptArgs @('--check') -EnvInfo $EnvInfo -Isolated -LogName 'build_v11.log')
if ($code -ne 0) {
    if ($ContinueOnBuildDiff) {
        Write-Warning "build_v11.py --check failed (exit $code). Continuing because -ContinueOnBuildDiff was set."
        Write-Warning "On Windows this is often CRLF (packaged) vs LF (builder). See GUIDE_Programs_Usage_v11_EN.md §5.4."
    } else {
        Write-Error @"
build_v11.py --check failed (exit $code).
On Windows, two files often differ only by line endings (CRLF in git vs LF from the builder): the reference Markdown and Item_Review_Register_v11.csv.
Re-run with -ContinueOnBuildDiff to finish validate + dashboard, or inspect programs/output/logs/build_v11.log.
"@
        exit $code
    }
}

Write-Host "=== [3/4] Structural validator ===" -ForegroundColor Cyan
$code = [int](Invoke-ProgramsPython -ScriptName 'validate_reference_v11.py' -EnvInfo $EnvInfo -Isolated -LogName 'validate_reference_v11.log')
if ($code -ne 0) { Write-Error "validate_reference_v11.py failed (exit $code)"; exit $code }

Write-Host "=== [4/4] HTML dashboard ===" -ForegroundColor Cyan
$code = [int](Invoke-ProgramsPython -ScriptName 'v11_html_dashboard.py' -EnvInfo $EnvInfo -Isolated -LogName 'dashboard_v11.log')
if ($code -ne 0) { Write-Error "v11_html_dashboard.py failed (exit $code)"; exit $code }

Copy-ValidationArtefacts -EnvInfo $EnvInfo -Config $Config
Write-Host ""
Write-Host "Technical checks completed. RELEASE STATUS MUST STILL BE READ FROM THE JSON REPORT." -ForegroundColor Yellow
Write-Host "Open $($EnvInfo.Referentiel)\validation_dashboard_v11.html or output\dashboards\." -ForegroundColor Yellow
exit 0
