import { detectChanges } from '../src/git/detector';
import { commitChanges } from '../src/git/committer';
import { classifyChanges } from '../src/analyzer/change-classifier';
import { buildCommitMessage } from '../src/generator/message-builder';

describe('Autocommit Workflow Integration Tests', () => {
    let changes;

    beforeEach(() => {
        // Setup code to initialize the repository state before each test
    });

    afterEach(() => {
        // Cleanup code to reset the repository state after each test
    });

    test('should detect changes in the repository', async () => {
        changes = await detectChanges();
        expect(changes).toBeDefined();
        expect(changes.length).toBeGreaterThan(0);
    });

    test('should classify detected changes', () => {
        const classifiedChanges = classifyChanges(changes);
        expect(classifiedChanges).toBeDefined();
        expect(classifiedChanges.additions).toBeGreaterThan(0);
    });

    test('should build a commit message from classified changes', () => {
        const message = buildCommitMessage(changes);
        expect(message).toMatch(/^(feat|fix|docs|style|refactor|perf|test|chore): .+/);
    });

    test('should commit changes to the repository', async () => {
        const message = buildCommitMessage(changes);
        const commitResult = await commitChanges(message);
        expect(commitResult).toBeTruthy();
    });
});