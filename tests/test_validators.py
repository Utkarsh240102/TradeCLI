import pytest
from decimal import Decimal
from bot.validators import (
    validate_symbol, validate_side, validate_order_type,
    validate_quantity, validate_price, validate_stop_price,
)

# --- Symbol Validators ---
def test_validate_symbol_uppercases():
    assert validate_symbol("btcusdt") == "BTCUSDT"

def test_validate_symbol_strips_whitespace():
    assert validate_symbol("  BTCUSDT  ") == "BTCUSDT"

def test_validate_symbol_empty_raises():
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_symbol("")

# --- Side Validators ---
def test_validate_side_buy():
    assert validate_side("buy") == "BUY"

def test_validate_side_sell():
    assert validate_side("SELL") == "SELL"

def test_validate_side_invalid_raises():
    with pytest.raises(ValueError, match="BUY or SELL"):
        validate_side("BUUY")

# --- Order Type Validators ---
def test_validate_order_type_market():
    assert validate_order_type("market") == "MARKET"

def test_validate_order_type_invalid_raises():
    with pytest.raises(ValueError, match="MARKET, LIMIT, or STOP_MARKET"):
        validate_order_type("LIMT")

# --- Quantity Validators ---
def test_validate_quantity_valid():
    assert validate_quantity("0.001") == Decimal("0.001")

def test_validate_quantity_negative_raises():
    with pytest.raises(ValueError, match="greater than 0"):
        validate_quantity("-1")

def test_validate_quantity_non_numeric_raises():
    with pytest.raises(ValueError, match="valid number"):
        validate_quantity("abc")

# --- Price Validators ---
def test_validate_price_none_for_market_returns_none():
    assert validate_price(None, "MARKET") is None

def test_validate_price_none_for_limit_raises():
    with pytest.raises(ValueError, match="required for LIMIT"):
        validate_price(None, "LIMIT")

def test_validate_price_valid():
    assert validate_price("45000.5", "LIMIT") == Decimal("45000.5")

# --- Stop Price Validators ---
def test_validate_stop_price_none_for_stop_market_raises():
    with pytest.raises(ValueError, match="required for STOP_MARKET"):
        validate_stop_price(None, "STOP_MARKET")

def test_validate_stop_price_valid():
    assert validate_stop_price("44000.0", "STOP_MARKET") == Decimal("44000.0")
