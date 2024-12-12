import * as vscode from 'vscode';

export class StatusBarService {
    private statusBarItem: vscode.StatusBarItem;

    constructor() {
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Left
        );
    }

    show(text: string) {
        this.statusBarItem.text = text;
        this.statusBarItem.show();
    }

    hide() {
        this.statusBarItem.hide();
    }
} 