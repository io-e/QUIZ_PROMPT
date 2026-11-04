# Common.ps1 — shared helpers for Math Diagnostic v11 program wrappers
# Dot-source from wrappers: . "$PSScriptRoot\..\lib\Common.ps1"

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-ProgramsRoot {
    return (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
}

function Get-ProgramsConfigPath {
    return (Join-Path (Get-ProgramsRoot) 'config\programs_v11.yaml')
}

function Import-ProgramsConfig {
    param(
        [string]$PythonExe = ''
    )
    $cfgPath = Get-ProgramsConfigPath
    if (-not (Test-Path -LiteralPath $cfgPath)) {
        throw "Config not found: $cfgPath"
    }
    $py = if ($PythonExe) { $PythonExe } else { 'py' }
    $code = @'
import json, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML missing. Install with: py -3 -m pip install PyYAML\n")
    sys.exit(2)
data = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8")) or {}
print(json.dumps(data, ensure_ascii=False))
'@
    $tmp = Join-Path $env:TEMP ("ea_eval_cfg_" + [guid]::NewGuid().ToString('N') + ".py")
    Set-Content -LiteralPath $tmp -Value $code -Encoding UTF8
    try {
        if ($PythonExe) {
            $json = & $PythonExe $tmp $cfgPath
        } else {
            $json = & py -3 $tmp $cfgPath
        }
        if ($LASTEXITCODE -ne 0) { throw "Failed to load YAML config (exit $LASTEXITCODE)" }
        return ($json | ConvertFrom-Json)
    } finally {
        Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
}

function Resolve-ProgramsPython {
    param(
        [string]$PythonExe = '',
        [object]$Config = $null
    )
    if ($PythonExe) {
        return $PythonExe
    }
    $root = Get-ProgramsRoot
    $candidates = @()
    if ($null -ne $Config -and $null -ne $Config.python -and $null -ne $Config.python.venv_candidates) {
        foreach ($rel in $Config.python.venv_candidates) {
            $candidates += (Join-Path $root $rel)
        }
    } else {
        $candidates += (Join-Path $root '.venv\Scripts\python.exe')
        $candidates += (Join-Path $root '..\.venv\Scripts\python.exe')
    }
    foreach ($c in $candidates) {
        if (Test-Path -LiteralPath $c) { return (Resolve-Path $c).Path }
    }
    $launcher = 'py'
    $ver = '-3'
    if ($null -ne $Config -and $null -ne $Config.python) {
        if ($Config.python.launcher) { $launcher = [string]$Config.python.launcher }
        if ($Config.python.version_arg) { $ver = [string]$Config.python.version_arg }
    }
    return "$launcher $ver"
}

function Get-ReferentielRoot {
    param([object]$Config)
    $root = Get-ProgramsRoot
    $rel = '..'
    if ($null -ne $Config -and $null -ne $Config.paths -and $Config.paths.referentiel) {
        $rel = [string]$Config.paths.referentiel
    }
    return (Resolve-Path (Join-Path $root $rel)).Path
}

function Get-OutputRoot {
    param([object]$Config)
    $root = Get-ProgramsRoot
    $rel = 'output'
    if ($null -ne $Config -and $null -ne $Config.paths -and $Config.paths.output) {
        $rel = [string]$Config.paths.output
    }
    $out = Join-Path $root $rel
    New-Item -ItemType Directory -Force -Path $out | Out-Null
    return (Resolve-Path $out).Path
}

function Initialize-ProgramsEnvironment {
    param(
        [object]$Config,
        [string]$PythonExe = ''
    )
    $ref = Get-ReferentielRoot -Config $Config
    $out = Get-OutputRoot -Config $Config
    $prog = Get-ProgramsRoot
    $env:EA_EVAL_REFERENTIEL = $ref
    $env:EA_EVAL_OUTPUT = $out
    $env:EA_EVAL_PROGRAMS = $prog
    foreach ($sub in @('validation', 'prompts', 'dashboards', 'demos', 'logs', 'builds')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $out $sub) | Out-Null
    }
    return [pscustomobject]@{
        Programs     = $prog
        Referentiel  = $ref
        Output       = $out
        Python       = (Resolve-ProgramsPython -PythonExe $PythonExe -Config $Config)
        Scripts      = (Join-Path $prog 'scripts')
        ConfigPath   = (Get-ProgramsConfigPath)
    }
}

function Invoke-ProgramsPython {
    param(
        [Parameter(Mandatory = $true)][string]$ScriptName,
        [string[]]$ScriptArgs = @(),
        [Parameter(Mandatory = $true)]$EnvInfo,
        [switch]$Isolated,
        [string]$LogName = ''
    )
    $scriptPath = Join-Path $EnvInfo.Scripts $ScriptName
    if (-not (Test-Path -LiteralPath $scriptPath)) {
        throw "Script not found: $scriptPath"
    }
    $pyArgs = @()
    $exe = [string]$EnvInfo.Python
    # Support "py -3" as a single string
    if ($exe -match '^(py)\s+(\S+)$') {
        $cmd = $Matches[1]
        $pyArgs += $Matches[2]
    } else {
        $cmd = $exe
    }
    if ($Isolated) { $pyArgs += '-I' }
    $pyArgs += $scriptPath
    if ($ScriptArgs) { $pyArgs += $ScriptArgs }

    Write-Host "→ $cmd $($pyArgs -join ' ')" -ForegroundColor Cyan
    Write-Host "  REFERENTIEL=$($EnvInfo.Referentiel)" -ForegroundColor DarkGray
    Write-Host "  OUTPUT=$($EnvInfo.Output)" -ForegroundColor DarkGray

    # Capture output and exit code first. Do not pipe the native call through
    # Tee-Object and then `return $LASTEXITCODE`: PowerShell functions emit every
    # uncaptured pipeline object, so callers receive log lines + the code and
    # treat the result as failure (e.g. "failed: 0 0").
    $output = & $cmd @pyArgs 2>&1
    $code = 0
    if ($null -ne $LASTEXITCODE) {
        $code = [int]$LASTEXITCODE
    }

    if ($LogName) {
        $log = Join-Path $EnvInfo.Output "logs\$LogName"
        $output | Set-Content -LiteralPath $log -Encoding UTF8
        Write-Host "  log: $log" -ForegroundColor DarkGray
    }
    if ($null -ne $output) {
        $output | Out-Host
    }
    return $code
}

function Copy-ValidationArtefacts {
    param(
        [Parameter(Mandatory = $true)]$EnvInfo,
        [object]$Config
    )
    $mirror = $true
    if ($null -ne $Config -and $null -ne $Config.outputs -and $null -ne $Config.outputs.mirror_validation_reports) {
        $mirror = [bool]$Config.outputs.mirror_validation_reports
    }
    if (-not $mirror) { return }
    $names = @(
        'validation_report_v11.json',
        'validation_report_v11.txt',
        'qa_v11.json',
        'Item_Release_Eligibility_v11.csv',
        'Coverage_Gaps_v11.csv',
        'validation_dashboard_v11.html',
        'tests_output_v11.txt',
        'validator_output_v11.txt'
    )
    if ($null -ne $Config -and $null -ne $Config.outputs -and $null -ne $Config.outputs.validation_glob) {
        $names = @($Config.outputs.validation_glob)
    }
    $dest = Join-Path $EnvInfo.Output 'validation'
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    foreach ($n in $names) {
        $src = Join-Path $EnvInfo.Referentiel $n
        if (Test-Path -LiteralPath $src) {
            Copy-Item -LiteralPath $src -Destination (Join-Path $dest $n) -Force
            Write-Host "  mirrored $n → output/validation/" -ForegroundColor DarkGray
        }
    }
}

function Test-ProgramsPrerequisites {
    param([Parameter(Mandatory = $true)]$EnvInfo)
    $exe = [string]$EnvInfo.Python
    $code = @'
import importlib.util, sys
missing = [m for m in ("sympy",) if importlib.util.find_spec(m) is None]
print(sys.version.split()[0])
if missing:
    print("MISSING:" + ",".join(missing))
    sys.exit(2)
print("OK")
'@
    $tmp = Join-Path $env:TEMP ("ea_eval_pre_" + [guid]::NewGuid().ToString('N') + ".py")
    Set-Content -LiteralPath $tmp -Value $code -Encoding UTF8
    try {
        if ($exe -match '^(py)\s+(\S+)$') {
            $out = & $Matches[1] $Matches[2] $tmp
        } else {
            $out = & $exe $tmp
        }
        Write-Host "Python: $($out | Select-Object -First 1)" -ForegroundColor Green
        if ($LASTEXITCODE -ne 0) {
            throw "Missing modules. Create a venv and install: pip install sympy==1.14.0 PyYAML"
        }
    } finally {
        Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
}

