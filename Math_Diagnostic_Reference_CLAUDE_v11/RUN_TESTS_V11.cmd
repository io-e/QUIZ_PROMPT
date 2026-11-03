@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PY=py -3"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

echo [1/4] Regression tests...
%PY% -I tests_v11.py > "tests_output_v11.txt" 2>&1
set "RESULT=%ERRORLEVEL%"
type "tests_output_v11.txt"
if not "%RESULT%"=="0" goto :failed

echo [2/4] Reproducible rebuild (check mode only; does not overwrite the review register)...
%PY% -I build_v11.py --check
if errorlevel 1 goto :failed

echo [3/4] Structural validator and release-status report...
%PY% -I validate_reference_v11.py > "validator_output_v11.txt" 2>&1
set "RESULT=%ERRORLEVEL%"
type "validator_output_v11.txt"
if not "%RESULT%"=="0" goto :failed

echo [4/4] Generate offline HTML dashboard...
%PY% -I v11_html_dashboard.py
if errorlevel 1 goto :failed

echo.
echo Technical checks completed. RELEASE STATUS MUST STILL BE READ FROM THE JSON REPORT.
echo The current 600-item set is not approved for release.
echo Open validation_dashboard_v11.html in a browser to see findings and HOLD reasons.
goto :done
:failed
echo.
echo ERROR: One of the test steps failed. Inspect the messages above.
:done
pause
