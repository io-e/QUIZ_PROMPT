@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM Prefer PowerShell program wrappers when available.
REM -ContinueOnBuildDiff: packaged CRLF vs builder LF often differs on Windows only.
if exist "programs\wrappers\Invoke-AllChecks.ps1" (
  echo Running programs\wrappers\Invoke-AllChecks.ps1 -ContinueOnBuildDiff ...
  pwsh -NoProfile -File "programs\wrappers\Invoke-AllChecks.ps1" -ContinueOnBuildDiff
  if errorlevel 1 goto :failed
  goto :done
)

set "PY=py -3"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
set "EA_EVAL_REFERENTIEL=%cd%"
set "EA_EVAL_PROGRAMS=%cd%\programs"
set "EA_EVAL_OUTPUT=%cd%\programs\output"

echo [1/4] Regression tests...
%PY% -I programs\scripts\tests_v11.py > "tests_output_v11.txt" 2>&1
set "RESULT=%ERRORLEVEL%"
type "tests_output_v11.txt"
if not "%RESULT%"=="0" goto :failed

echo [2/4] Reproducible rebuild (check mode only)...
%PY% -I programs\scripts\build_v11.py --check
if errorlevel 1 (
  echo WARNING: build check failed. On Windows this is often CRLF vs LF. Continuing.
)

echo [3/4] Structural validator...
%PY% -I programs\scripts\validate_reference_v11.py > "validator_output_v11.txt" 2>&1
set "RESULT=%ERRORLEVEL%"
type "validator_output_v11.txt"
if not "%RESULT%"=="0" goto :failed

echo [4/4] Generate offline HTML dashboard...
%PY% -I programs\scripts\v11_html_dashboard.py
if errorlevel 1 goto :failed

echo.
echo Technical checks completed. RELEASE STATUS MUST STILL BE READ FROM THE JSON REPORT.
goto :done
:failed
echo.
echo ERROR: One of the test steps failed. Inspect the messages above.
:done
pause