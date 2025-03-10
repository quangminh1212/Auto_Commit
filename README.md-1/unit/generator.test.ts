import { buildCommitMessage } from '../../src/generator/message-builder';

describe('Message Builder', () => {
    it('should generate a commit message for added files', () => {
        const changes = [
            { type: 'added', file: 'file1.txt' },
            { type: 'added', file: 'file2.txt' }
        ];
        const message = buildCommitMessage(changes);
        expect(message).toBe('Add: file1.txt, file2.txt');
    });

    it('should generate a commit message for modified files', () => {
        const changes = [
            { type: 'modified', file: 'file3.txt' }
        ];
        const message = buildCommitMessage(changes);
        expect(message).toBe('Modify: file3.txt');
    });

    it('should generate a commit message for deleted files', () => {
        const changes = [
            { type: 'deleted', file: 'file4.txt' }
        ];
        const message = buildCommitMessage(changes);
        expect(message).toBe('Delete: file4.txt');
    });

    it('should handle mixed changes correctly', () => {
        const changes = [
            { type: 'added', file: 'file5.txt' },
            { type: 'modified', file: 'file6.txt' },
            { type: 'deleted', file: 'file7.txt' }
        ];
        const message = buildCommitMessage(changes);
        expect(message).toBe('Add: file5.txt; Modify: file6.txt; Delete: file7.txt');
    });

    it('should return a default message for no changes', () => {
        const changes = [];
        const message = buildCommitMessage(changes);
        expect(message).toBe('No changes detected');
    });
});