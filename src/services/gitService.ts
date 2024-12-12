import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class GitService {
    private getFileType(filePath: string): string {
        if (filePath.match(/\.(md|txt)$/)) return 'docs';
        if (filePath.match(/\.(ts|js|py|java)$/)) return 'feat';
        if (filePath.match(/\.(test|spec)\./)) return 'test';
        return 'chore';
    }

    async createCommit(uri: vscode.Uri) {
        try {
            const relativePath = vscode.workspace.asRelativePath(uri);
            const fileType = this.getFileType(relativePath);
            const message = `${fileType}: update ${relativePath}`;

            await execAsync(`git add "${relativePath}"`);
            await execAsync(`git commit -m "${message}"`);

            vscode.window.showInformationMessage(`Created commit: ${message}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to create commit: ${error}`);
        }
    }

    async push() {
        try {
            await execAsync('git push');
            vscode.window.showInformationMessage('Changes pushed to remote');
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to push changes: ${error}`);
        }
    }
} 