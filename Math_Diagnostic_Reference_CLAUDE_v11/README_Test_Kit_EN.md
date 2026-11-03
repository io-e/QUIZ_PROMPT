# Math Diagnostic v11 — Windows Test Kit

This archive contains the **original Claude v11 package without modifying its source files**, plus a hands-on guide, a Windows test runner, and two standalone HTML examples.

## Start on Windows

1. Extract the full ZIP.
2. Open the directory `Math_Diagnostic_Reference_CLAUDE_v11`.
3. Open PowerShell in that directory and install SymPy in a local Python environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install "sympy==1.14.0"
   ```

4. Double-click **`RUN_TESTS_V11.cmd`**.
5. Open **`validation_dashboard_v11.html`** for release gates and row-level HOLD reasons.
6. Open **`diagnostic_prototype_v11.html`** to test the local HTML quiz demonstration.

Read **`GUIDE_Math_Diagnostic_v11_Testing_and_HTML_EN.md`** for all commands, CSV review procedures, interpretation and HTML-generation steps.

**Current status:** structural PASS, paper HOLD, digital HOLD. The prototype is *not approved for student assessment*. It does not validate YAML against the production quiz-player schema.
