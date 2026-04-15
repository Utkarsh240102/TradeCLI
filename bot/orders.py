import logging

from bot.client import BinanceClient
from bot.validators import (
    validate_symbol, validate_side, validate_quantity,
    validate_price, validate_stop_price,
)

logger = logging.getLogger("trading_bot.orders")


def _format_response(raw: dict) -> dict:
    """Extract the specific fields the assignment requires in output."""
    return {
        "orderId":      raw.get("orderId", "N/A"),
        "symbol":       raw.get("symbol", "N/A"),
        "status":       raw.get("status", "N/A"),
        "side":         raw.get("side", "N/A"),
        "type":         raw.get("type", "N/A"),
        "executedQty":  raw.get("executedQty", "0"),
        "avgPrice":     raw.get("avgPrice", raw.get("price", "N/A")),
        "cumQuote":     raw.get("cumQuote", "N/A"),
    }
