# Auto Commit

A tool to automatically commit changes to a git repository at regular intervals or when changes are detected.

## Features

- Monitor directories for changes
- Automatically commit changes at specified intervals
- Customizable commit messages with time/date placeholders
- Can run once or continuously monitor

## Installation

1. Clone this repository
2. Make sure Git is installed and available in your PATH
3. Run `python setup.py` to verify requirements

## Usage

```bash
python main.py [options]
```

### Options

- `--watch, -w`: Directory to watch for changes (default: current directory)
- `--interval, -i`: Commit interval in minutes (default: 60)
- `--message, -m`: Commit message template (default: "Auto commit at {datetime}")
- `--once`: Commit once and exit

### Message Placeholders

You can use the following placeholders in commit messages:
- `{datetime}`: Current date and time (format: YYYY-MM-DD HH:MM:SS)
- `{date}`: Current date (format: YYYY-MM-DD)
- `{time}`: Current time (format: HH:MM:SS)

## Examples

```bash
# Monitor current directory, commit every 30 minutes
python main.py --interval 30

# Watch specific directory with custom commit message
python main.py --watch /path/to/project --message "Auto saved at {time}"

# Commit once and exit
python main.py --once
```

## Configuration

Edit the `config.py` file to customize:
- Default commit frequency
- Default message templates
- Default watch directory

## Requirements

- Git installed and configured
- Python 3.6 or higher

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.