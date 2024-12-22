import typer
from rich import print
from pathlib import Path

from auto_commit.core.watcher import FileWatcher
from auto_commit.config.settings import load_config

app = typer.Typer()

@app.command()
def start(
    config_path: Path = typer.Option(
        "config/settings.yaml",
        "--config",
        "-c",
        help="Path to config file"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging"
    )
):
    """Start watching directory for changes"""
    try:
        config = load_config(config_path)
        watcher = FileWatcher(config)
        print(f"[green]Started watching {config['watch_path']}[/green]")
        watcher.start()
    except KeyboardInterrupt:
        print("\n[yellow]Stopping watcher...[/yellow]")
    except Exception as e:
        print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 