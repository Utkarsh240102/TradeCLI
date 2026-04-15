# Binance Futures Testnet Trading Bot

A professional-grade, pure-Python Command-Line Interface (CLI) for executing programmatic trades on the Binance Futures Testnet. It features native HMAC SHA-256 request signing, a strictly decoupled MVC-style architecture, and a beautiful, strictly-typed terminal output using Typer and Rich.

## 🌟 Key Features
- **Zero Heavy Abstractions**: Avoids bulky wrappers like `python-binance`. Utilizes native Python `hashlib` and `requests` for explicit REST API interaction.
- **Precision First**: Uses exact JSON-first error parsing directly from Binance headers to prevent silent failures and generic stack traces.
- **Robust Local Validation**: Validates user inputs (Symbol formats, Sides, Order Types, and Prices) locally in pure Python *before* attempting network requests, saving latency and API rate limits.
- **Dual-Handler Logging**: Simultaneously outputs clean, colorized info logs to the Rich console, whilst streaming granular DEBUG network traffic into `logs/trading_bot.log`.
- **Elegant User Interface**: Implements `typer` arguments and options to build a highly intuitive CLI interface.

## 📋 Prerequisites
Before running the bot, ensure you have:
1. Python 3.10+ installed.
2. A **Binance Testnet Account** (Futures). Generate your free API keys by heading to the [Binance Mock Trading](https://testnet.binancefuture.com/) portal and logging in with a test account.

## 🏗️ Project Architecture
The codebase strictly separates concerns into logic layers:
- `bot/validators.py`: Handles pure string and numeric validations natively.
- `bot/client.py`: Manages internet transport, secure `.env` credential loading, millisecond timestamp generation, and the core HMAC signature algorithm.
- `bot/orders.py`: The business logic layer. Composes routing instructions (Market, Limit, Stop Market), dictates parameters like `timeInForce="GTC"`, and prepares REST payloads.
- `cli.py`: The user-interface root. It initializes Typer, manages Rich color schemes, parses command arguments, and handles graceful exits for both API and network errors.

## 🚀 Setup Instructions

1. **Clone the repository & Navigate to folder**
   ```bash
   git clone <your-repo-url>
   cd TradeCLI
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows (PowerShell):
   .\venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The project explicitly pins `click==8.1.7` for `typer` compatibility).*

4. **Environment Variables**
   Duplicate `.env.example` to `.env` and map your credentials securely:
   ```env
   BINANCE_API_KEY="your_testnet_api_key_here"
   BINANCE_API_SECRET="your_testnet_api_secret_here"
   BINANCE_BASE_URL="https://testnet.binancefuture.com"
   ```

## 💻 Usage & CLI Commands

You can always invoke the `--help` flag for a breakdown of argument requirements:
```bash
python cli.py place-order --help
```

**1. Place a Market Order (Instant Fill)**
```bash
# syntax: python cli.py place-order <SYMBOL> <SIDE> MARKET <QTY>
python cli.py place-order BTCUSDT BUY MARKET 0.001
```

**2. Place a Limit Order (Rests on Order Book)**
```bash
# Requires the --price / -p flag
python cli.py place-order ETHUSDT SELL LIMIT 0.05 --price 3500.50
```

**3. Place a Stop Market Order (Trigger Condition)**
```bash
python cli.py place-order SOLUSDT BUY STOP_MARKET 1.0 --price 160.00
```

## 🔍 Logging and Error Handling
- **Debugging**: If something fails, open `logs/trading_bot.log`. The bot automatically streams the exact payload dicts, exact query strings, and exact timestamps sent to Binance in real-time.
- **Fail Gracefully**: If you trigger a Binance error (e.g., `-1102`), the console will elegantly display a bold red message summarizing the error directly from Binance's servers, rather than printing an unreadable 50-line Python Traceback.

## 🧪 Running Tests
This project uses Pytest for local unit assurance on all validators and numerical logic. Ensure you have the virtual environment activated, then run:

```bash
pytest tests/ -v
```
*(Confirms validations for symbols, zero-quantity orders, step sizes, and formatting).*
