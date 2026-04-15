import hmac
import hashlib
import logging
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv


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
