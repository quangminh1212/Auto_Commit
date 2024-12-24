import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def main(
    config: str = typer.Option("config/settings.yaml", "--config", "-c"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """Auto Commit Tool"""
    print(f"Starting with config: {config}")
    print(f"Verbose mode: {verbose}")

def run():
    app()

if __name__ == "__main__":
    run() 