import * as vscode from 'vscode';

export class ConfigService {
    private getConfig() {
        return vscode.workspace.getConfiguration('autoCommit');
    }

    getDelay(): number {
        return this.getConfig().get('delay', 30);
    }

    getAutoPush(): boolean {
        return this.getConfig().get('autoPush', false);
    }

    isEnabled(): boolean {
        return this.getConfig().get('enabled', false);
    }
} 