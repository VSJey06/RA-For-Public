# VS Code Extension Guide

## Installation

### From VSIX
1. Download `RA.vsix` from [vscode/](../vscode/)
2. Open VS Code
3. Press `Ctrl+Shift+P`
4. Select `Extensions: Install from VSIX...`
5. Choose the downloaded `RA.vsix`

### From Marketplace
Search for "RA Language" in the VS Code extensions panel.

## Features

- Syntax highlighting
- Code snippets
- LSP integration (diagnostics, completion, hover)
- Debugger support
- Project templates

## Usage

Open any `.ra` file to activate the extension. Create a new project:

```bash
radk new my-project
cd my-project
code .
```
