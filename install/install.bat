@echo off
REM RA Language Installer (Batch)
REM Usage: install.bat

echo Downloading RA Language Setup...
powershell -Command "& { Invoke-WebRequest -Uri 'https://github.com/RA-Lang/RA/releases/latest/download/RA_Setup.exe' -OutFile '%TEMP%\RA_Setup.exe' }"
if %ERRORLEVEL% neq 0 (
    echo Download failed. Check your internet connection.
    exit /b 1
)
echo Running installer...
start /wait "" "%TEMP%\RA_Setup.exe"
echo RA Language installation complete!
echo Run 'ra --version' to verify.
