# Installation Guide

## Windows

### Option 1: Installer
1. Download `RA_Setup.exe` from [installers](../installers/)
2. Run the installer and follow the prompts
3. RA is added to your PATH automatically

### Option 2: Portable (USB-ready)
1. Download `RA.exe` from [downloads/Release](../downloads/Release/)
2. Place in any folder
3. Run from command prompt

### Option 3: PowerShell
```powershell
powershell -ExecutionPolicy Bypass -File install/install.ps1
```

## Linux / macOS

```bash
chmod +x install/install.sh
./install/install.sh
```

## Verification

```bash
ra --version
```

Expected output:
```
RA Language v1.0.0
```
