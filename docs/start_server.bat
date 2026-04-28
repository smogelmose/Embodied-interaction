@echo off
title Metamorphic Efforts Server
cd /d "%~dp0"

echo.
echo   ========================================
echo     Metamorphic Efforts Server
echo     http://localhost:8080
echo     Press Ctrl+C to stop
echo   ========================================
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    python -m http.server 8080
    goto :end
)

where python3 >nul 2>nul
if %errorlevel%==0 (
    python3 -m http.server 8080
    goto :end
)

echo Python not found. Trying PowerShell...
echo.
powershell -ExecutionPolicy Bypass -Command ^
    "$listener = New-Object System.Net.HttpListener; $listener.Prefixes.Add('http://localhost:8080/'); $listener.Start(); Write-Host 'Server running on http://localhost:8080'; Write-Host 'Press Ctrl+C to stop'; $root = (Get-Location).Path; while ($listener.IsListening) { $ctx = $listener.GetContext(); $path = $ctx.Request.Url.LocalPath; if ($path -eq '/') { $path = '/index.html' }; $file = Join-Path $root $path.Replace('/', '\'); if (Test-Path $file) { $bytes = [System.IO.File]::ReadAllBytes($file); $ext = [System.IO.Path]::GetExtension($file).ToLower(); $mime = @{'.html'='text/html';'.js'='application/javascript';'.css'='text/css';'.mp3'='audio/mpeg';'.wav'='audio/wav';'.jpg'='image/jpeg';'.png'='image/png';'.json'='application/json';'.csv'='text/csv'}; if ($mime[$ext]) { $ctx.Response.ContentType = $mime[$ext] } else { $ctx.Response.ContentType = 'application/octet-stream' }; $ctx.Response.ContentLength64 = $bytes.Length; $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length) } else { $ctx.Response.StatusCode = 404 }; $ctx.Response.Close() }"

:end
pause
