# Auto Commit with Copilot

This project provides two methods to automate the commit process in VS Code with Copilot:
1. Using a PowerShell script with a keyboard shortcut
2. Using a VS Code extension

## Quick Setup (One Step Only)

To install and set up everything in a single step, run the `auto-commit-setup.bat` file:

```
.\auto-commit-setup.bat
```

This script will automatically:
1. Check and guide you to install necessary tools (VS Code, Node.js, Inno Setup)
2. Install vsce and dependencies
3. Compile TypeScript
4. Package the extension into a VSIX file
5. Create an EXE installer (if Inno Setup is installed)
6. Install the extension into VS Code (if you choose to)

> **Note**: It's recommended to run the script with Administrator privileges to ensure a smooth installation process.

## Method 1: PowerShell Script

### Features

When you press the shortcut `Ctrl+Alt+C`, the script will automatically:
1. Open the Source Control panel
2. Call the Generate Commit Message with Copilot command
3. Perform the commit

### Installation

1. Make sure you have VS Code and GitHub Copilot installed
2. Clone this repository
3. Open the project in VS Code
4. The shortcut `Ctrl+Alt+C` is already configured in the `.vscode/keybindings.json` file

### How to Use

1. Make changes to your project
2. Stage the changes you want to commit
3. Press `Ctrl+Alt+C` to automatically generate a commit message and perform the commit

### Requirements

- Visual Studio Code
- GitHub Copilot
- PowerShell

## Method 2: VS Code Extension

### Features

This extension provides a command and shortcut to automatically:
1. Open the Source Control panel
2. Call the Generate Commit Message with Copilot command
3. Perform the commit

### How to Use

1. Make changes to your project
2. Stage the changes you want to commit
3. Use one of the following methods:
   - Press the shortcut `Ctrl+Space` (Windows/Linux) or `Cmd+Space` (Mac)
   - Right-click in the editor and select "Auto Commit with Copilot" from the context menu
   - Open the Command Palette (Ctrl+Shift+P) and type "Auto Commit with Copilot"

### Requirements

- Visual Studio Code 1.60.0 or later
- GitHub Copilot extension installed and configured
- Node.js and npm

## Uninstalling the Extension

1. Open VS Code
2. Press Ctrl+Shift+X to open the Extensions view
3. Find "Auto Commit with Copilot" in the list of installed extensions
4. Click the "Uninstall" button

## Customization

- Method 1: You can edit the `scripts/auto-commit.ps1` file to change the behavior of the script or change the shortcut in the `.vscode/keybindings.json` file.
- Method 2: You can edit the extension source code in the `extension/src` directory.

## Detailed Instructions

See the `USER_GUIDE.md` file for more details on how to use the scripts and tools. 