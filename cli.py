import typer
from rich.console import Console
import logging
from bot.logging_config import setup_logging
from bot.client import BinanceClient
from bot.orders import place_market_order, place_limit_order, place_stop_market_order
from bot import BinanceAPIError, NetworkError

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
    console.print(
        Panel(
            rich_json,
            title=f"[bold blue]{title}[/bold blue]",
            expand=False))


@app.callback()
def main():
    """
    This callback runs before any command.
    We use it to set up our logging configuration.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("CLI initialized and logging configured.")


@app.command()
def place_order(symbol: str = typer.Argument(...,
                                             help="Trading pair symbol (e.g., BTCUSDT)"),
                side: str = typer.Argument(...,
                                           help="Order side: BUY or SELL"),
                order_type: str = typer.Argument(...,
                                                 help="Order type: MARKET, LIMIT, or STOP_MARKET"),
                quantity: str = typer.Argument(...,
                                               help="Order quantity in base asset"),
                price: str = typer.Option(None,
                                          "--price",
                                          "-p",
                                          help="Limit price (required for LIMIT)"),
                stop_price: str = typer.Option(None,
                                               "--stop-price",
                                               "-s",
                                               help="Stop price / Trigger price (required for STOP_MARKET)"),
                ):
    """
    Place a new order on Binance Futures Testnet.
    """
    logger = logging.getLogger(__name__)

    side = side.upper()
    order_type = order_type.upper()

    if side not in ["BUY", "SELL"]:
        print_error("Side must be BUY or SELL")
        raise typer.Exit(code=1)

    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        print_error("Order type must be MARKET, LIMIT, or STOP_MARKET")
        raise typer.Exit(code=1)

    if order_type == "LIMIT" and price is None:
        print_error("Price is required for LIMIT orders.")
        raise typer.Exit(code=1)

    if order_type == "STOP_MARKET" and stop_price is None:
        print_error("Stop price is required for STOP_MARKET orders.")
        raise typer.Exit(code=1)

    try:
        client = BinanceClient()
        logger.info(
            f"Attempting to place {order_type} {side} order for {quantity} {symbol}.")

        if order_type == "MARKET":
            response = place_market_order(
                client, symbol=symbol, side=side, quantity=quantity)
        elif order_type == "LIMIT":
            response = place_limit_order(
                client,
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price)
        elif order_type == "STOP_MARKET":
            response = place_stop_market_order(
                client,
                symbol=symbol,
                side=side,
                quantity=quantity,
                stop_price=stop_price)

        print_success(
            f"Order successfully placed! Order ID: {
                response.get(
                    'orderId',
                    'Unknown')}")
        print_json_response(response, title="Order Details")

    except BinanceAPIError as e:
        print_error(f"Binance API Rejected the Order: {str(e)}")
        logger.error(f"API Error during `place_order`: {e}")
        raise typer.Exit(code=1)
    except NetworkError as e:
        print_error(f"Network issue: {str(e)}")
        logger.error(f"Network Error during `place_order`: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        logger.exception("Unexpected error in `place_order`")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
