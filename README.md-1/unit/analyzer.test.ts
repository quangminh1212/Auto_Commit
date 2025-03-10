import { classifyChange } from '../../src/analyzer/change-classifier';

describe('Change Classifier', () => {
    test('should classify added lines correctly', () => {
        const changes = {
            added: ['line 1', 'line 2'],
            removed: [],
            modified: []
        };
        const result = classifyChange(changes);
        expect(result).toBe('Addition');
    });

    test('should classify removed lines correctly', () => {
        const changes = {
            added: [],
            removed: ['line 1', 'line 2'],
            modified: []
        };
        const result = classifyChange(changes);
        expect(result).toBe('Deletion');
    });

    test('should classify modified lines correctly', () => {
        const changes = {
            added: [],
            removed: [],
            modified: ['line 1 modified']
        };
        const result = classifyChange(changes);
        expect(result).toBe('Modification');
    });

    test('should classify mixed changes correctly', () => {
        const changes = {
            added: ['line 1'],
            removed: ['line 2'],
            modified: ['line 3 modified']
        };
        const result = classifyChange(changes);
        expect(result).toBe('Mixed');
    });

    test('should return Unknown for no changes', () => {
        const changes = {
            added: [],
            removed: [],
            modified: []
        };
        const result = classifyChange(changes);
        expect(result).toBe('Unknown');
    });
});