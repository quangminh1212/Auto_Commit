import * as vscode from 'vscode';

interface CommitHistory {
    timestamp: number;
    message: string;
    files: string[];
}

/**
 * Tracks and manages commit history
 * Uses: In-memory storage with size limit
 */
export class HistoryService {
    private static readonly MAX_HISTORY = 100;
    private history: CommitHistory[] = [];

    /**
     * Adds new commit to history
     * @param message - Commit message
     * @param files - Array of changed files
     * 
     * Implements: FIFO queue with max size
     * Storage: In-memory array
     */
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