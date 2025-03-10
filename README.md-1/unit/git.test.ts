// This file contains unit tests for the git detection and committing functionalities to ensure they work as expected.

import { detectChanges } from '../src/git/detector';
import { commitChanges } from '../src/git/committer';

describe('Git Detection and Committing', () => {
    test('should detect changes in the git repository', () => {
        const changes = detectChanges();
        expect(changes).toBeDefined();
        expect(Array.isArray(changes)).toBe(true);
    });

    test('should commit changes to the git repository', () => {
        const changes = detectChanges();
        if (changes.length > 0) {
            const commitMessage = 'Test commit message';
            const result = commitChanges(commitMessage);
            expect(result).toBe(true);
        } else {
            console.warn('No changes detected to commit.');
        }
    });
});