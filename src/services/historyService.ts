import * as vscode from 'vscode';

interface CommitHistory {
    timestamp: number;
    message: string;
    files: string[];
}

export class HistoryService {
    private static readonly MAX_HISTORY = 100;
    private history: CommitHistory[] = [];

    addCommit(message: string, files: string[]) {
        this.history.unshift({
            timestamp: Date.now(),
            message,
            files
        });

        if (this.history.length > HistoryService.MAX_HISTORY) {
            this.history.pop();
        }
    }

    getRecentCommits(limit: number = 10): CommitHistory[] {
        return this.history.slice(0, limit);
    }

    clearHistory() {
        this.history = [];
    }
} 