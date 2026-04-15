from typer.testing import CliRunner
from cli import app
from unittest.mock import patch
from bot import BinanceAPIError, NetworkError

runner = CliRunner()


@patch("cli.place_market_order")
@patch("cli.BinanceClient")
def test_place_order_market_success(mock_client, mock_place_order):
    """Test that a market order works properly."""
    # Simulate a successful response from our business layer
    mock_place_order.return_value = {"orderId": 555, "status": "NEW"}

    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "BUY", "MARKET", "0.05"])

    assert result.exit_code == 0
    assert "✓ SUCCESS" in result.stdout
    assert "555" in result.stdout


def test_place_order_invalid_order_type():
    """Test that specifying an invalid order type throws an error."""
    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "BUY", "TRAILING_STOP", "0.05"])

    assert result.exit_code == 1
    assert "Order type must be MARKET, LIMIT, or STOP_MARKET" in result.stdout
    assert "✗ ERROR" in result.stdout


@patch("cli.place_stop_market_order")
@patch("cli.BinanceClient")
def test_place_order_stop_market_success(mock_client, mock_stop):
    """Test that a STOP_MARKET order triggers properly."""
    mock_stop.return_value = {"orderId": 999, "status": "NEW"}

    result = runner.invoke(app,
                           ["place-order",
                            "BTCUSDT",
                            "SELL",
                            "STOP_MARKET",
                            "0.05",
                            "--stop-price",
                            "40000"])

    assert result.exit_code == 0
    assert "✓ SUCCESS" in result.stdout
    assert "999" in result.stdout


@patch("cli.place_market_order")
@patch("cli.BinanceClient")
def test_place_order_generic_exception(mock_client, mock_market):
    """Test how CLI handles a completely unhandled Exception."""
    mock_market.side_effect = Exception("System meltdown!")

    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "BUY", "MARKET", "0.05"])

    assert result.exit_code == 1
    assert "An unexpected error occurred: System meltdown!" in result.stdout
    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "HODL", "MARKET", "0.05"])

    assert result.exit_code == 1
    assert "Side must be BUY or SELL" in result.stdout
    assert "✗ ERROR" in result.stdout


def test_place_order_limit_missing_price():
    """Test that placing a LIMIT order without a price fails."""
    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "SELL", "LIMIT", "0.05"])

    assert result.exit_code == 1
    assert "Price is required for LIMIT orders" in result.stdout


@patch("cli.place_limit_order")
@patch("cli.BinanceClient")
def test_place_order_api_error(mock_client, mock_limit):
    """Test how CLI handles a BinanceAPIError."""
    # Force the mock to throw an exception
    mock_limit.side_effect = BinanceAPIError(-1102, "Margin is insufficient")

    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "SELL", "LIMIT", "0.05", "--price", "50000"])

    assert result.exit_code == 1
    assert "Binance API Rejected the Order" in result.stdout
    assert "-1102" in result.stdout


@patch("cli.place_market_order")
@patch("cli.BinanceClient")
def test_place_order_network_error(mock_client, mock_market):
    """Test how CLI handles a NetworkError."""
    mock_market.side_effect = NetworkError("Cannot connect to Binance")

    result = runner.invoke(
        app, ["place-order", "BTCUSDT", "BUY", "MARKET", "0.05"])

    assert result.exit_code == 1
    assert "Network issue: Cannot connect" in result.stdout
