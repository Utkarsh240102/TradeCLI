import hmac
import hashlib
import logging
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot import BinanceAPIError, NetworkError


class BinanceClient:
    def __init__(self) -> None:
        """Initialize the client session, load credentials, and check configuration."""
        # Load the variables from the .env file
        load_dotenv()
        
        # Read the keys into memory
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

        # Validation: If the keys are missing or still the default placeholders from .env.example
        if not self.api_key or not self.api_secret or self.api_key == "your_testnet_api_key_here":
            raise ValueError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env\n"
                "Copy .env.example to .env and fill in your testnet credentials."
            )

        # Create a persistent HTTP session for efficiency
        self.session = requests.Session()
        
        # Connect to the centralized logger we built earlier
        self.logger = logging.getLogger("trading_bot.client")

    def _get_timestamp(self) -> int:
        """Return the current time in milliseconds (required by Binance)."""
        return int(time.time() * 1000)

    def _sign(self, query_string: str) -> str:
        """Generate an HMAC SHA256 signature using the API secret."""
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def post(self, endpoint: str, params: dict) -> dict:
        """Send a signed POST request to the Binance testnet."""
        # 1. Prepare mandatory security parameters
        params["timestamp"] = self._get_timestamp()
        params["recvWindow"] = 5000

        # 2. Build and sign the query string
        query_string = urlencode(params)
        signature = self._sign(query_string)
        signed_query = query_string + "&signature=" + signature

        # Log request parameters (Safe: API secret is never logged)
        self.logger.debug(f"POST {endpoint} params={params}")

        # 3. Fire the request over the network
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                data=signed_query,  # Binance expects form data, not JSON body
                headers={"X-MBX-APIKEY": self.api_key},
                timeout=10
            )
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout: POST {endpoint}")
            raise NetworkError("Request timed out after 10s. Check your internet connection.")
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error: POST {endpoint}")
            raise NetworkError("Cannot connect to Binance testnet. Check your internet connection.")

        # 4. Extract data and gracefully handle Binance errors
        try:
            data = response.json()
        except ValueError:
            self.logger.error(f"Non-JSON response [{response.status_code}]: {response.text[:200]}")
            raise NetworkError(f"Binance returned non-JSON response (HTTP {response.status_code}).")

        self.logger.debug(f"Response {response.status_code}: {data}")

        # Check if Binance successfully received the request but deliberately rejected the trade
        if isinstance(data, dict) and data.get("code", 0) < 0:
            self.logger.error(f"Binance API error [{data['code']}]: {data['msg']}")
            raise BinanceAPIError(data["code"], data["msg"])

        # Check for standard HTTP 4xx/5xx crashes not caught above
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            self.logger.error(f"HTTP {response.status_code}: {response.text[:200]}")
            raise NetworkError(f"Unexpected HTTP {response.status_code} from Binance.")

        return data
