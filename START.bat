@echo off
echo ========================================
echo   AIRA - Artificial Intelligence Research Assistant
echo   Created by Joss Collen
echo ========================================
echo.
echo Starting AIRA...
echo.
echo Open http://localhost:5000 in your browser
echo.

:: Get the directory of this batch file
set AIRA_DIR=%~dp0
echo AIRA Directory: %AIRA_DIR%
echo.

:: Try to find Python
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Using system Python...
    python "%AIRA_DIR%start_aira.py"
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        echo Using python3...
        python3 "%AIRA_DIR%start_aira.py"
    ) else (
        echo ERROR: Python not found!
        echo Please install Python from https://www.python.org
        pause
        exit /b 1
    )
)

pause
