# RA Language Installer (PowerShell)
# Run: powershell -ExecutionPolicy Bypass -File install.ps1

param(
    [string]$Version = "latest",
    [switch]$Portable,
    [switch]$Help
)

if ($Help) {
    Write-Host "RA Language Installer" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\install.ps1 [-Version latest] [-Portable] [-Help]"
    Write-Host ""
    Write-Host "  -Version    Version to install (default: latest)"
    Write-Host "  -Portable   Download portable version instead of installer"
    Write-Host "  -Help       Show this help message"
    exit 0
}

$RepoUrl = "https://github.com/RA-Lang/RA/releases"
$InstallDir = "$env:LOCALAPPDATA\RA"

if ($Portable) {
    Write-Host "Downloading RA Portable..." -ForegroundColor Yellow
    $Url = "$RepoUrl/download/$Version/RA_Portable-$Version-windows-x86_64.zip"
    $ZipPath = "$env:TEMP\RA_Portable.zip"
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath
    Expand-Archive -Path $ZipPath -DestinationPath $InstallDir -Force
    Write-Host "Installed to: $InstallDir" -ForegroundColor Green
} else {
    Write-Host "Downloading RA Setup..." -ForegroundColor Yellow
    $Url = "$RepoUrl/download/$Version/RA_Setup.exe"
    $SetupPath = "$env:TEMP\RA_Setup.exe"
    Invoke-WebRequest -Uri $Url -OutFile $SetupPath
    Start-Process -FilePath $SetupPath -Wait
}

Write-Host "RA Language installation complete!" -ForegroundColor Green
Write-Host "Run 'ra --version' to verify." -ForegroundColor Cyan
