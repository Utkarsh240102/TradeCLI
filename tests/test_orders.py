from unittest.mock import MagicMock
from bot.orders import (
    _format_response,
    place_market_order,
    place_limit_order,
    place_stop_market_order
)


def test_format_response():
    """Test that the response formatter keeps only relevant keys."""
    raw_response = {
        "orderId": 12345,
        "symbol": "BTCUSDT",
        "status": "NEW",
        "side": "BUY",
        "type": "MARKET",
        "executedQty": "0.000",
        "avgPrice": "0.00",
        "cumQuote": "0.000",
        "clientOrderId": "ignore_this",
        "timeInForce": "GTC"
    }

    formatted = _format_response(raw_response)

    assert "orderId" in formatted
    assert "status" in formatted
    assert "clientOrderId" not in formatted
    assert len(formatted.keys()) == 8


def test_place_market_order():
    """Test that place_market_order passes correct params to the client."""
    mock_client = MagicMock()
    mock_client.post.return_value = {"orderId": 111, "symbol": "ETHUSDT"}

    place_market_order(mock_client, "ETHUSDT", "BUY", "0.05")

    # Assert post was called exactly once
    mock_client.post.assert_called_once()

    # Assert the params sent to post were exactly correct
    called_args = mock_client.post.call_args[0]

    assert called_args[0] == "/fapi/v1/order"
    assert called_args[1]["symbol"] == "ETHUSDT"
    assert called_args[1]["type"] == "MARKET"
    assert called_args[1]["quantity"] == "0.05"
    assert "timeInForce" not in called_args[1]


def test_place_limit_order():
    """Test that place_limit_order correctly injects timeInForce and price."""
    mock_client = MagicMock()
    mock_client.post.return_value = {"orderId": 222, "symbol": "BTCUSDT"}

    place_limit_order(
        mock_client, "BTCUSDT", "SELL", "0.1", "50000")

    called_args = mock_client.post.call_args[0]

    assert called_args[1]["type"] == "LIMIT"
    assert called_args[1]["timeInForce"] == "GTC"
    assert called_args[1]["price"] == "50000"


def test_place_stop_market_order():
    """Test that place_stop_market_order correctly injects stopPrice."""
    mock_client = MagicMock()
    mock_client.post.return_value = {"orderId": 333, "symbol": "BTCUSDT"}

    place_stop_market_order(
        mock_client, "BTCUSDT", "SELL", "0.1", "40000")

    called_args = mock_client.post.call_args[0]

    assert called_args[1]["type"] == "STOP_MARKET"
    assert called_args[1]["stopPrice"] == "40000"
