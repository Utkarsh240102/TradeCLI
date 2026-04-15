import typer
from rich.console import Console
import logging
from bot.logging_config import setup_logging

# Initialize Typer App and Rich Console
app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

def print_success(message: str):
    """Displays a success message in green."""
    console.print(f"[bold green]✓ SUCCESS:[/bold green] {message}")

def print_error(message: str):
    """Displays an error message in red."""
    console.print(f"[bold red]✗ ERROR:[/bold red] {message}")

def print_json_response(data: dict, title: str = "Response"):
    """Displays formatted JSON data."""
    from rich.panel import Panel
    from rich.json import JSON
    import json
    
    json_str = json.dumps(data)
    rich_json = JSON(json_str)
    console.print(Panel(rich_json, title=f"[bold blue]{title}[/bold blue]", expand=False))

@app.callback()
def main():
    """
    This callback runs before any command.
    We use it to set up our logging configuration.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("CLI initialized and logging configured.")

if __name__ == "__main__":
    app()
