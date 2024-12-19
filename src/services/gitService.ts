import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';
import { HistoryService } from './historyService';
import { CommitTemplateService } from './commitTemplateService';

const execAsync = promisify(exec);

export class GitService {
    private historyService: HistoryService;
    private templateService: CommitTemplateService;
    private pendingChanges: Map<string, NodeJS.Timeout> = new Map();

    constructor() {
        this.historyService = new HistoryService();
        this.templateService = new CommitTemplateService();
    }

    private async getGitRoot(): Promise<string> {
        try {
            const { stdout } = await execAsync('git rev-parse --show-toplevel');
            return stdout.trim();
        } catch (error) {
            throw new Error('Not a git repository');
        }
    }

    private async getChangedFiles(): Promise<string[]> {
        const { stdout } = await execAsync('git status --porcelain');
        return stdout.split('\n')
            .filter(line => line.trim())
            .map(line => line.slice(3));
    }

    /**
     * Watches file changes and creates commits automatically
     * @param uri - File URI that was changed
     * @param details - Optional commit details
     * @returns Promise<void>
     * 
     * Uses: child_process.exec to run git commands
     * Pattern: Observer pattern for file changes
     */
    async createCommit(uri: vscode.Uri, details?: string) {
        try {
            const relativePath = vscode.workspace.asRelativePath(uri);
            const fileType = this.getFileType(relativePath);
            const message = this.templateService.generateMessage(
                fileType,
                relativePath,
                details
            );

            await execAsync(`git add "${relativePath}"`);
            await execAsync(`git commit -m "${message}"`);

            this.historyService.addCommit(message, [relativePath]);
            
            vscode.window.showInformationMessage(`Created commit: ${message}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to create commit: ${error}`);
        }
    }

    /**
     * Groups multiple file changes into a single commit
     * @param delay - Time to wait before creating batch commit
     * @returns Promise<void>
     * 
     * Strategy: Groups files by type (feat, fix, docs, etc)
     * Uses: git status to get changed files
     */
    async batchCommit(delay: number = 30) {
        const changedFiles = await this.getChangedFiles();
        if (changedFiles.length === 0) return;

        const filesByType = this.groupFilesByType(changedFiles);
        
        for (const [type, files] of filesByType) {
            const message = this.templateService.generateMessage(
                type,
                files.length > 1 ? `multiple ${type} files` : files[0]
            );

            await execAsync(`git add ${files.join(' ')}`);
            await execAsync(`git commit -m "${message}"`);
            
            this.historyService.addCommit(message, files);
        }
    }

    private groupFilesByType(files: string[]): Map<string, string[]> {
        const groups = new Map<string, string[]>();
        
        files.forEach(file => {
            const type = this.getFileType(file);
            if (!groups.has(type)) {
                groups.set(type, []);
            }
            groups.get(type)?.push(file);
        });

        return groups;
    }

    /**
     * Determines the type of change based on file extension
     * @param filePath - Path to the changed file
     * @returns string - Commit type (feat, fix, docs, etc)
     * 
     * Rules:
     * - .md, .txt -> docs
     * - .ts, .js, .py -> feat
     * - test files -> test
     * - others -> chore
     */
    private getFileType(filePath: string): string {
        if (filePath.match(/\.(md|txt)$/)) return 'docs';
        if (filePath.match(/\.(ts|js|py|java)$/)) return 'feat';
        if (filePath.match(/\.(test|spec)\./)) return 'test';
        return 'chore';
    }

    /**
     * Pushes commits to remote repository
     * @returns Promise<void>
     * 
     * Uses: git push command
     * Handles: Branch detection and error cases
     */
    async push() {
        try {
            const branch = await this.getCurrentBranch();
            await execAsync(`git push origin ${branch}`);
            vscode.window.showInformationMessage(
                `Changes pushed to ${branch}`
            );
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to push: ${error}`);
        }
    }

    private async getCurrentBranch(): Promise<string> {
        const { stdout } = await execAsync('git branch --show-current');
        return stdout.trim();
    }
} 