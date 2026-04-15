import pytest
import responses
import os
from unittest.mock import patch
from bot.client import BinanceClient
from bot import BinanceAPIError, NetworkError
import requests

@pytest.fixture
def mock_env(monkeypatch):
    """Mock the .env variables so we don't need real keys to run tests."""
    monkeypatch.setenv("BINANCE_API_KEY", "test_key")
    monkeypatch.setenv("BINANCE_API_SECRET", "test_secret")
    monkeypatch.setenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

def test_client_init_missing_keys(monkeypatch):
    """Test that the client raises an error if API keys are missing."""
    monkeypatch.delenv("BINANCE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="BINANCE_API_KEY and BINANCE_API_SECRET must be set"):
        BinanceClient()

def test_get_timestamp(mock_env):
    """Test that _get_timestamp returns a valid integer timestamp."""
    client = BinanceClient()
    ts = client._get_timestamp()
    assert isinstance(ts, int)
    assert ts > 1600000000000  # Basic sanity check for a valid MS timestamp

def test_sign(mock_env):
    """Test HMAC SHA256 signature generation."""
    client = BinanceClient()
    query_string = "symbol=BTCUSDT&side=BUY&type=MARKET&quantity=0.001&timestamp=123456789"
    # Using 'test_secret' as the key, the expected hash is deterministic
    signature = client._sign(query_string)
    assert isinstance(signature, str)
    assert len(signature) == 64

@responses.activate
def test_post_success(mock_env):
    """Test a successful POST request to Binance."""
    client = BinanceClient()
    
    # Mock the Binance Response
    responses.add(
        responses.POST,
        "https://testnet.binancefuture.com/fapi/v1/order",
        json={"orderId": 12345, "symbol": "BTCUSDT", "status": "NEW"},
        status=200
    )
    
    res = client.post("/fapi/v1/order", {"symbol": "BTCUSDT"})
    
    assert res["orderId"] == 12345
    assert res["status"] == "NEW"

@responses.activate
def test_post_binance_api_error(mock_env):
    """Test how the client handles Binance-specific JSON errors (e.g., -1102)."""
    client = BinanceClient()
    
    responses.add(
        responses.POST,
        "https://testnet.binancefuture.com/fapi/v1/order",
        json={"code": -1102, "msg": "Mandatory parameter 'timeInForce' was not sent, was empty/null..."},
        status=400
    )
    
    with pytest.raises(BinanceAPIError) as exc_info:
        client.post("/fapi/v1/order", {"symbol": "BTCUSDT"})
        
    assert "[-1102]" in str(exc_info.value)
    assert "Mandatory parameter" in str(exc_info.value)

@patch("requests.Session.post")
def test_post_network_timeout(mock_post, mock_env):
    """Test how the client handles a network timeout."""
    mock_post.side_effect = requests.exceptions.Timeout()
    client = BinanceClient()
    
    with pytest.raises(NetworkError, match="Request timed out after 10s"):
        client.post("/fapi/v1/order", {"symbol": "BTCUSDT"})