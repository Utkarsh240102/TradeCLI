from decimal import Decimal, InvalidOperation


def validate_symbol(symbol: str) -> str:
    """Uppercase and strip. Raises ValueError if empty."""
    cleaned = symbol.strip().upper()
    if not cleaned:
        raise ValueError("Symbol cannot be empty. Example: BTCUSDT")
    return cleaned


def validate_side(side: str) -> str:
    """Accepts 'buy'/'sell' case-insensitively. Raises ValueError otherwise."""
    cleaned = side.strip().upper()
    if cleaned not in ("BUY", "SELL"):
        raise ValueError(f"Side must be BUY or SELL, got: '{side}'")
    return cleaned


def validate_order_type(order_type: str) -> str:
    """Accepts MARKET, LIMIT, STOP_MARKET case-insensitively."""
    cleaned = order_type.strip().upper()
    if cleaned not in ("MARKET", "LIMIT", "STOP_MARKET"):
        raise ValueError(f"Order type must be MARKET, LIMIT, or STOP_MARKET, got: '{order_type}'")
    return cleaned


def validate_quantity(quantity: str) -> Decimal:
    """Parses to Decimal. Raises ValueError if non-numeric or <= 0."""
    try:
        qty = Decimal(quantity.strip())
    except InvalidOperation:
        raise ValueError(f"Quantity must be a valid number, got: '{quantity}'")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0, got: {qty}")
    return qty


def validate_price(price: str | None, order_type: str) -> Decimal | None:
    """Required for LIMIT. Optional for MARKET. Raises ValueError if missing for LIMIT."""
    if price is None:
        if order_type.upper() == "LIMIT":
            raise ValueError("Price is required for LIMIT orders. Use --price flag.")
        return None
    try:
        p = Decimal(price.strip())
    except InvalidOperation:
        raise ValueError(f"Price must be a valid number, got: '{price}'")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0, got: {p}")
    return p


def validate_stop_price(stop_price: str | None, order_type: str) -> Decimal | None:
    """Required for STOP_MARKET orders. Raises ValueError if missing."""
    if stop_price is None:
        if order_type.upper() == "STOP_MARKET":
            raise ValueError("Stop price is required for STOP_MARKET orders. Use --stop-price flag.")
        return None
    try:
        sp = Decimal(stop_price.strip())
    except InvalidOperation:
        raise ValueError(f"Stop price must be a valid number, got: '{stop_price}'")
    if sp <= 0:
        raise ValueError(f"Stop price must be greater than 0, got: {sp}")
    return sp


def round_to_step(value: Decimal, step: str) -> Decimal:
    """Round value DOWN to the nearest step increment (for stepSize/tickSize compliance)."""
    from decimal import ROUND_DOWN
    step_dec = Decimal(step)
    return (value / step_dec).to_integral_value(rounding=ROUND_DOWN) * step_dec
