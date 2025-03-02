# Auto Commit with Copilot - User Guide

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

## Using the Extension

1. Make changes to your project
2. Stage the changes you want to commit
3. Press the shortcut `Ctrl+Space` to automatically:
   - Open the Source Control panel
   - Generate a commit message with Copilot
   - Perform the commit

## Uninstalling the Extension

### Method 1: Using the Script

Run the `uninstall-extension.bat` file to uninstall the extension:
```
.\uninstall-extension.bat
```

### Method 2: From VS Code

1. Open VS Code
2. Press Ctrl+Shift+X to open the Extensions view
3. Find "Auto Commit with Copilot" in the list of installed extensions
4. Click the "Uninstall" button

## Alternative Method: PowerShell Script

In addition to the extension, this project also provides a PowerShell script to automate the commit process.

### Features

When you press the shortcut `Ctrl+Alt+C`, the script will automatically:
1. Open the Source Control panel
2. Call the Generate Commit Message with Copilot command
3. Perform the commit

### How to Use

1. Make changes to your project
2. Stage the changes you want to commit
3. Press `Ctrl+Alt+C` to automatically generate a commit message and perform the commit

### Requirements

- Visual Studio Code
- GitHub Copilot
- PowerShell

## Project Structure

- `auto-commit-setup.bat`: Main script to install and set up everything
- `uninstall-extension.bat`: Script to uninstall the extension
- `create-installer.iss`: Inno Setup configuration file to create the EXE installer
- `install-extension.bat`: Script to install the extension from the VSIX file
- `extension/`: Directory containing the extension source code
  - `src/`: TypeScript source code
  - `package.json`: Extension configuration
- `scripts/`: Directory containing PowerShell scripts

## Customization

- **PowerShell Script**: You can edit the `scripts/auto-commit.ps1` file to change the behavior of the script or change the shortcut in the `.vscode/keybindings.json` file.
- **Extension**: You can edit the extension source code in the `extension/src` directory. 