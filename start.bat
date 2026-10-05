@echo off
REM ZEYRECUITE - local-first launcher (Windows)
setlocal
cd /d "%~dp0"

REM Prefer a venv at the project root, then backend/.venv, else create one at root.
if exist ".venv\Scripts\python.exe" (
    set PY=.venv\Scripts\python.exe
) else if exist "backend\.venv\Scripts\python.exe" (
    set PY=backend\.venv\Scripts\python.exe
) else (
    echo [setup] Creating virtual environment...
    python -m venv .venv
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    set PY=.venv\Scripts\python.exe
)

echo [setup] Ensuring dependencies...
"%PY%" -m pip install -q -r backend\requirements.txt

echo.
echo ============================================================
echo   ZEYRECUITE is starting...
echo   Open:  http://127.0.0.1:8000
echo   Stop:  press Ctrl+C in this window
echo ============================================================
echo.
"%PY%" -m uvicorn zeyrecuite.app:create_app --factory --app-dir backend --host 127.0.0.1 --port 8000

endlocal
