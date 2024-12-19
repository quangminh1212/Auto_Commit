import * as vscode from 'vscode';

/**
 * Manages commit message templates and generation
 * Uses: Conventional Commits specification
 * https://www.conventionalcommits.org/
 */
export class CommitTemplateService {
    private templates: Map<string, string> = new Map([
        ['feat', 'feat: add {filename}'],
        ['fix', 'fix: resolve issue in {filename}'],
        ['docs', 'docs: update documentation for {filename}'],
        ['style', 'style: format {filename}'],
        ['refactor', 'refactor: improve code structure in {filename}'],
        ['test', 'test: add tests for {filename}'],
        ['chore', 'chore: update {filename}']
    ]);

    getTemplate(type: string): string {
        return this.templates.get(type) || '{type}: update {filename}';
    }

    /**
     * Generates commit message from template
     * @param type - Commit type (feat, fix, etc)
     * @param filename - Changed file name
     * @param details - Optional additional details
     * @returns string - Formatted commit message
     * 
     * Template format: <type>: <description>
     * Example: "feat: add user authentication"
     */
    generateMessage(type: string, filename: string, details?: string): string {
        let message = this.getTemplate(type).replace('{filename}', filename);
        if (details) {
            message += `\n\n${details}`;
        }
        return message;
    }
} 