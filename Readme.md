# Binance Futures Testnet Trading Bot

A Python Command-Line Interface (CLI) application for executing programmatic trades on the Binance Futures Testnet (USDT-M). This project implements native HMAC SHA-256 request signing, adheres to a decoupled, layered architecture, includes unit tests for core validation logic, and provides clear terminal output.

## Features & Capabilities
- **Native Implementation:** Places Market and Limit orders on Binance Futures Testnet directly via REST HTTP requests. Validates input and gracefully handles exceptions.
- **Bonus Feature:** Successfully implemented **STOP_MARKET** orders requiring dynamic trigger payload construction.
- **Interactive CLI UX:** Utilizes Typer and Rich to build a clean terminal output, including pre-execution order request summaries, formatted JSON response tables, and readable error states.

## Architecture & Project Structure
The codebase strictly follows a modular, layered structure to separate concerns effectively:
```text
TradeCLI/
├── bot/
│   ├── __init__.py
│   ├── client.py          # HTTP transport, timestamping, HMAC SHA-256 signature logic 
│   ├── orders.py          # Business logic (Market, Limit, Stop Market payload creation)
│   ├── validators.py      # Input validation for symbols, prices, and quantities
│   └── logging_config.py  # Dual-handler logger (Console + File)
├── cli.py                 # Typer application root, argument parsing, and UI presentation
├── tests/                 # Pytest suite 
├── logs/                  # Directory for outputting trading_bot.log
├── .env                   # Environment variables (API credentials)
├── .flake8                # Linter configuration
├── requirements.txt       # Project dependencies
└── Readme.md              # You are here
```

## Prerequisites
1. **Python 3.10+** installed on your system.
2. A **Binance Futures Testnet Account**. Generate your API keys by logging into the [Binance Mock Trading](https://testnet.binancefuture.com/) portal.

## Setup Instructions

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd TradeCLI
```

**2. Create & Activate a Virtual Environment**
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**
Copy `.env.example` to a new file named `.env` and add your Testnet credentials:
```env
BINANCE_API_KEY="your_testnet_api_key_here"
BINANCE_API_SECRET="your_testnet_api_secret_here"
BINANCE_BASE_URL="https://testnet.binancefuture.com"
```

## Usage & CLI Commands

Access the integrated help menu at any time:
```bash
python cli.py place-order --help
```

### 1. Place a MARKET Order
Execute immediately at the best available market price. Displays an order request summary before execution.
```bash
# Syntax: cli.py place-order <SYMBOL> <SIDE> MARKET <QTY>
python cli.py place-order BTCUSDT BUY MARKET 0.01
```

### 2. Place a LIMIT Order
Requires the `--price` (`-p`) option flag. The order rests until the market reaches your target. Displays an order request summary before execution.
```bash
python cli.py place-order BTCUSDT SELL LIMIT 0.01 --price 75000
```

### 3. Place a STOP_MARKET Order (Bonus)
Requires the `--price` (`-p`) option flag, which natively acts as the `stopPrice` parameter payload. Displays an order request summary before execution.
```bash
python cli.py place-order ETHUSDT SELL STOP_MARKET 0.05 --price 3000
```

## Logging & Error Handling
- **Dual-Logging System:** 
  - **Console:** Provides an active order request summary beforehand, followed by clear success tables cleanly separated from network noise.
  - **File (`logs/trading_bot.log`):** Actively captures raw HTTP POST requests, timestamps, parameter payloads, and full API JSON responses for auditing.
- **Graceful Failures:** If Binance rejects an order (e.g., limit price out of bounds), the CLI intercepts the exact error code (like `-4024`) from the JSON body and displays a readable error block, avoiding arbitrary Python Tracebacks.

## Testing & Quality Assurance
Run the included test and linting suite to verify component logic.

**1. Unit Testing**
```bash
pytest --cov=bot --cov=cli tests/
```

**2. Static Type Checking**
```bash
mypy bot/ cli.py
```

**3. Code Linting**
```bash
flake8 bot/ cli.py tests/
```

## Key Assumptions & Design Choices
- **USDT-Margined Futures Framework:** The bot interacts explicitly with the `/fapi/v1/order` endpoint for USDT-M futures on the Binance Testnet.
- **Time in Force:** LIMIT orders automatically inject `timeInForce="GTC"` (Good 'Til Canceled) into the payload as it is mandatory for resting limit orders on Binance's backend.
- **Server-Side Precision Validation:** To minimize latency and overhead, the bot validates basic types but allows Binance's server to act as the ultimate source of truth for numeric precision requirements (lot sizes/tick sizes). It returns any server limits elegantly back to the user via the CLI output.