import typer
from pathlib import Path
from rich import print
import yaml

from auto_commit.core.watcher import FileWatcher
from auto_commit.config.settings import load_config

app = typer.Typer()

@app.command()
def main(
    config: str = typer.Option("config/settings.yaml", "--config", "-c"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """Auto Commit Tool"""
    try:
        # Kiểm tra file config tồn tại
        config_path = Path(config)
        if not config_path.exists():
            print("[red]Error: Config file not found![/red]")
            raise typer.Exit(1)

        # Load config
        settings = load_config(config_path)
        
        # Khởi tạo và chạy watcher
        watcher = FileWatcher(settings)
        print(f"[green]Started watching {settings['watch_path']}[/green]")
        print("[yellow]Press Ctrl+C to stop...[/yellow]")
        
        # Bắt đầu theo dõi
        watcher.start()
        
    except KeyboardInterrupt:
        print("\n[yellow]Stopping watcher...[/yellow]")
    except Exception as e:
        print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

def run():
    app()

if __name__ == "__main__":
    run() 