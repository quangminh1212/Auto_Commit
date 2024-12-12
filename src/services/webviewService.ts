import * as vscode from 'vscode';
import { HistoryService } from './historyService';

export class WebviewService {
    private panel: vscode.WebviewPanel | undefined;
    private historyService: HistoryService;

    constructor(historyService: HistoryService) {
        this.historyService = historyService;
    }

    show() {
        if (this.panel) {
            this.panel.reveal();
            return;
        }

        this.panel = vscode.window.createWebviewPanel(
            'autoCommitHistory',
            'Auto Commit History',
            vscode.ViewColumn.One,
            {
                enableScripts: true
            }
        );

        this.updateContent();

        this.panel.onDidDispose(() => {
            this.panel = undefined;
        });
    }

    private updateContent() {
        if (!this.panel) return;

        const history = this.historyService.getRecentCommits();
        
        this.panel.webview.html = `
            <!DOCTYPE html>
            <html>
                <head>
                    <style>
                        body { padding: 20px; }
                        .commit { 
                            margin-bottom: 10px;
                            padding: 10px;
                            border: 1px solid #ccc;
                        }
                    </style>
                </head>
                <body>
                    <h2>Recent Commits</h2>
                    ${history.map(commit => `
                        <div class="commit">
                            <div>${commit.message}</div>
                            <small>${new Date(commit.timestamp).toLocaleString()}</small>
                        </div>
                    `).join('')}
                </body>
            </html>
        `;
    }
} 