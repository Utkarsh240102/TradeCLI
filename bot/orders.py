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


def place_market_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: str,
) -> dict:
    """Place a MARKET order. Returns formatted response dict."""
    # 1. Validate the user input strictly
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_qty = validate_quantity(quantity)

    # 2. Construct the exact parameters expected by Binance
    params = {
        "symbol":   clean_symbol,
        "side":     clean_side,
        "type":     "MARKET",
        "quantity": str(clean_qty),
    }

    # 3. Log our intent to the terminal/file before hitting the network
    logger.info(f"Placing MARKET {clean_side} {clean_qty} {clean_symbol}")
    
    # 4. Send the request
    response = client.post("/fapi/v1/order", params)
    
    # 5. Format and return the result
    formatted = _format_response(response)
    logger.info(f"Order placed. ID: {formatted['orderId']} | Status: {formatted['status']}")
    
    return formatted


def place_limit_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    quantity: str,
    price: str,
) -> dict:
    """Place a LIMIT GTC order. Returns formatted response dict."""
    # 1. Validate the user input strictly
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_qty = validate_quantity(quantity)
    clean_price = validate_price(price, "LIMIT")

    # 2. Construct the exact parameters expected by Binance
    params = {
        "symbol":      clean_symbol,
        "side":        clean_side,
        "type":        "LIMIT",
        "quantity":    str(clean_qty),
        "price":       str(clean_price),
        "timeInForce": "GTC",   # Required for LIMIT orders — omitting causes -1102
    }

    # 3. Log our intent to the terminal/file before hitting the network
    logger.info(f"Placing LIMIT {clean_side} {clean_qty} {clean_symbol} @ {clean_price}")
    
    # 4. Send the request
    response = client.post("/fapi/v1/order", params)
    
    # 5. Format and return the result
    formatted = _format_response(response)
    logger.info(f"Order placed. ID: {formatted['orderId']} | Status: {formatted['status']}")
    
    return formatted

