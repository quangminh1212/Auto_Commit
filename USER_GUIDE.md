# User Guide for Auto Commit

This guide explains how to use the Auto Commit tool effectively.

## Getting Started

### Installation

1. Download the latest release from the releases page
2. Run the installer for your platform:
   - Windows: `auto-commit-setup.bat`
   - MacOS/Linux: `./auto-commit-setup.sh`
3. Follow the on-screen instructions

### Basic Configuration

After installation, create or edit the `config.json` file:

```json
{
  "repositories": [
    {
      "path": "/path/to/your/repo",
      "frequency": "1h",
      "commitMessage": "Auto commit: {date} {changes}"
    }
  ],
  "defaultFrequency": "2h",
  "defaultCommitMessage": "Auto commit: {date}",
  "gitPath": "",
  "excludePatterns": ["node_modules", ".git", "*.log"]
}
```

## Command Reference

### Starting Auto Commit

```
auto-commit start [options]
```

Options:
- `--path, -p`: Repository path
- `--frequency, -f`: Commit frequency (e.g., "30m", "1h", "1d")
- `--message, -m`: Commit message template

### Managing Services

```
auto-commit service [install|remove|start|stop]
```

### Other Commands

- `auto-commit status`: View current status
- `auto-commit list`: List all monitored repositories
- `auto-commit help`: Show help information

## Advanced Features

### Custom Commit Messages

You can use these placeholders in your commit messages:
- `{date}`: Current date/time
- `{changes}`: Summary of changes
- `{files}`: Number of changed files

### Scheduling

Set specific schedules using cron syntax:

```json
{
  "schedule": "0 */2 * * *"  // Every 2 hours
}
```

## Troubleshooting

- **Issue**: Service won't start
  **Solution**: Check that Git is properly installed and in your PATH

- **Issue**: No commits are happening
  **Solution**: Verify your repository path and permissions

## Support

For additional help, file an issue on our GitHub repository. 