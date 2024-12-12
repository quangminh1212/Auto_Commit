import * as vscode from 'vscode';

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

    generateMessage(type: string, filename: string, details?: string): string {
        let message = this.getTemplate(type).replace('{filename}', filename);
        if (details) {
            message += `\n\n${details}`;
        }
        return message;
    }
} 