# RAPM Package Manager Guide

RAPM is the RA package manager for installing and managing libraries.

## Basic Commands

| Command | Description |
|---------|-------------|
| `rapm search <query>` | Search packages |
| `rapm install <package>` | Install a package |
| `rapm list` | List installed packages |
| `rapm update <package>` | Update a package |
| `rapm remove <package>` | Uninstall a package |

## Example

```bash
rapm search calculator
rapm install math-utils
rapm list
```

## Package Registry

RAPM uses the official RA package registry at `registry.ra-lang.org`.

## Publishing

```bash
rapm publish ./my-package
```

Requires a valid `ra-package.toml` manifest.
