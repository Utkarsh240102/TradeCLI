# Binance Futures Testnet Trading Bot

A professional-grade, pure-Python Command-Line Interface (CLI) for executing programmatic trades on the Binance Futures Testnet (USDT-M). Built to satisfy the PrimeTrade.ai Application Task, this project features native HMAC SHA-256 request signing, a strictly decoupled MVC-style architecture, comprehensive test coverage, and a beautiful, strictly-typed terminal output using Typer and Rich.

## 🎯 Assignment Completion & Bonus Features Achieved
- **Core Requirements:** Places Market and Limit orders (BUY/SELL) on Binance Futures Testnet natively via HTTP (no bulky `python-binance` wrappers). Validates input and gracefully handles exceptions.
- **Bonus 1 (3rd Order Type):** Successfully implemented **STOP_MARKET** orders requiring dynamic trigger payload construction.
- **Bonus 2 (Enhanced CLI UX):** Utilized **Typer** and **Rich** to build a stunning, color-coded terminal UI with formatted JSON tables and readable error states.

## 🏗️ Project Architecture
The codebase strictly follows the assignment's suggested decoupled structure to separate concerns:
```text
TradeCLI/
├── bot/
│   ├── __init__.py
│   ├── client.py          # HTTP transport, timestamping, HMAC SHA-256 signature logic 
│   ├── orders.py          # Business logic (Market, Limit, Stop Market payload creation)
│   ├── validators.py      # Input validation for symbols, prices, and quantities
│   └── logging_config.py  # Dual-handler logger (Rich Console + File)
├── cli.py                 # Typer application root, argument parsing, and UI presentation
├── tests/                 # Comprehensive Pytest suite simulating all local logic
├── logs/                  # Ignored directory for outputting trading_bot.log
├── .env                   # Environment variables (API credentials)
├── .flake8                # Linter configuration
├── requirements.txt       # Project dependencies
└── Readme.md              # You are here
```

## 📋 Prerequisites
1. **Python 3.10+** installed on your system.
2. A **Binance Futures Testnet Account**. Generate your API keys by logging into the [Binance Mock Trading](https://testnet.binancefuture.com/) portal.

## 🚀 Setup Instructions

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

## 💻 Usage & CLI Commands

Access the integrated help menu at any time:
```bash
python cli.py place-order --help
```

### 1. Place a MARKET Order (Instant Fill)
Executes immediately at the best available market price.
```bash
# Syntax: cli.py place-order <SYMBOL> <SIDE> MARKET <QTY>
python cli.py place-order BTCUSDT BUY MARKET 0.01
```

### 2. Place a LIMIT Order (Rests on Order Book)
Requires the `--price` (`-p`) flag. The order rests until the market reaches your target.
```bash
python cli.py place-order BTCUSDT SELL LIMIT 0.01 --price 75000
```

### 3. Place a STOP_MARKET Order (Trigger Condition)
Requires the `--price` (`-p`) flag, which natively acts as the `stopPrice` parameter payload.
```bash
python cli.py place-order ETHUSDT SELL STOP_MARKET 0.05 --price 3000
```

## 🔍 Logging & Error Handling
- **Dual-Logging System**: 
  - **Console:** The user sees elegant, color-coded success tables and simple summaries cleanly separated from network noise.
  - **File (`logs/trading_bot.log`):** Actively captures raw HTTP POST requests, precise timestamps, parameter payloads, and full API JSON responses for auditing.
- **Graceful Failures:** If Binance rejects an order (e.g., limit price out of bounds), the CLI intercepts the exact error code (like `-4024`) from the JSON body and displays a highly readable red formatting block, completely avoiding arbitrary Python Tracebacks.

## 🧪 Development, QA & Testing
This project was built with production-grade quality assurance in mind.

**1. Unit Testing (Near 100% Coverage)**
```bash
pytest --cov=bot --cov=cli tests/
```
All validators, client payloads, and order logic are fully covered.

**2. Static Type Checking**
```bash
mypy bot/ cli.py
```

**3. Code Linting (PEP-8)**
```bash
flake8 bot/ cli.py tests/
```

## 💡 Key Assumptions
- **USDT-Margined Futures Framework**: As per the core objective, this bot interacts explicitly with the `/fapi/v1/order` endpoint for USDT-M futures on the Binance Testnet.
- **Time in Force**: LIMIT orders automatically inject `timeInForce="GTC"` (Good 'Til Canceled) into the payload as it is mandatory for resting limit orders on Binance's backend.
- **Server-Side Precision Validation**: To significantly minimize latency and overhead (avoiding scraping and caching Exchange Info tick-sizes locally), the bot allows Binance's server to act as the ultimate source of truth for numeric precision requirements (lot sizes/tick sizes), returning any server rejections elegantly back to the user via the CLI format.