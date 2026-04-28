@echo off
title Metamorphic Efforts Docs Server
cd /d "%~dp0"

echo.
echo   ========================================
echo     Metamorphic Efforts Docs Server
echo     Serving: docs/
echo     http://localhost:8080/Metamorphic_Efforts.html
echo     Press Ctrl+C to stop
echo   ========================================
echo.

if not exist "docs\Metamorphic_Efforts.html" (
    echo Could not find docs\Metamorphic_Efforts.html
    echo Make sure the docs folder is populated first.
    goto :end
)

where python >nul 2>nul
if %errorlevel%==0 (
    python -m http.server 8080 -d docs
    goto :end
)

where python3 >nul 2>nul
if %errorlevel%==0 (
    python3 -m http.server 8080 -d docs
    goto :end
)

echo Python not found in PATH.
echo Install Python 3 and rerun this script.

:end
pause
