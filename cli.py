import typer
from rich.console import Console
import logging
from bot.logging_config import setup_logging

# Initialize Typer App and Rich Console
app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

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
