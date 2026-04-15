class BinanceAPIError(Exception):
    """Raised when Binance returns a negative error code in the response body."""
    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg
        super().__init__(f"[{code}] {msg}")


class NetworkError(Exception):
    """Raised when the request fails to reach the server (timeout, connection refused, non-JSON)."""
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)
