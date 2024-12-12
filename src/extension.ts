import * as vscode from 'vscode';
import { GitService } from './services/gitService';
import { ConfigService } from './services/configService';
import { StatusBarService } from './services/statusBar';

export function activate(context: vscode.ExtensionContext) {
    const configService = new ConfigService();
    const gitService = new GitService();
    const statusBar = new StatusBarService();

    let fileWatcher: vscode.FileSystemWatcher | undefined;
    let commitTimeout: NodeJS.Timeout | undefined;

    // Enable auto commit
    let enableCommand = vscode.commands.registerCommand('auto-commit.enable', () => {
        if (fileWatcher) {
            return;
        }

        fileWatcher = vscode.workspace.createFileSystemWatcher('**/*');
        
        fileWatcher.onDidChange(async (uri) => {
            if (commitTimeout) {
                clearTimeout(commitTimeout);
            }

            commitTimeout = setTimeout(async () => {
                await gitService.createCommit(uri);
                if (configService.getAutoPush()) {
                    await gitService.push();
                }
            }, configService.getDelay() * 1000);
        });

        statusBar.show('Auto Commit: Enabled');
        vscode.window.showInformationMessage('Auto Commit enabled');
    });

    // Disable auto commit
    let disableCommand = vscode.commands.registerCommand('auto-commit.disable', () => {
        if (fileWatcher) {
            fileWatcher.dispose();
            fileWatcher = undefined;
        }
        if (commitTimeout) {
            clearTimeout(commitTimeout);
        }
        statusBar.show('Auto Commit: Disabled');
        vscode.window.showInformationMessage('Auto Commit disabled');
    });

    context.subscriptions.push(enableCommand, disableCommand);
}

export function deactivate() {} 