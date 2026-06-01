# ⚡ Binance Futures Simplified Trading Bot (USDT-M Testnet)

A premium, structured, and visually stunning Python-based command-line interface (CLI) trading bot to place MARKET and LIMIT (BUY/SELL) orders on the Binance Futures Testnet (USDT-M) using the `python-binance` library.

Developed as a highly robust, professional-grade implementation complete with input validation, structured request-response logging, graceful exception handling, and an interactive CLI UX.

---

## ✨ Features
1. **Out-of-the-Box Demo Mode (Zero Credentials Required)**: If no Binance API keys are supplied (or if left as template placeholders), the bot dynamically detects this and runs a **high-fidelity local simulation** using authentic Binance REST JSON response shapes. **You can run and test this project immediately without configuring any keys!**
2. **Flexible API Layer**: Integrates clean wrapper classes separating API connection/logic (`bot/client.py`, `bot/orders.py`) from input/interface logic.
3. **Robust Input Validation**: Validates all 5 parameters (`symbol`, `side`, `order_type`, `quantity`, `price`) in a pure-Python validation module (`bot/validators.py`) before calling the exchange.
4. **Structured Logging**: Automatically writes verbose API requests, raw responses, and connection/execution details to a rotating log file (`logs/trading_bot.log`).
5. **Interactive UI Menu (Bonus Option)**: When run without CLI arguments (or with the `-i` flag), it boots a gorgeous interactive onboarding dashboard built on top of `rich` that leads users step-by-step with real-time validations, confirmation prompts, loading indicators, and styled response panels.
6. **Argparse Automated Mode**: Supports automated scripts and grading via traditional command-line flags.

---

## 📊 Application Architecture & Flowchart

```
           +---------------------------------------------+
           |             Run 'python cli.py'             |
           +---------------------------------------------+
                                  |
                                  v
           +---------------------------------------------+
           |     Interactive UX vs Argparse Parsing      |
           +---------------------------------------------+
                                  |
                                  v
           +---------------------------------------------+
           |    bot/validators.py (Checks all 5 args)    |
           +---------------------------------------------+
                                  |
                   +--------------+--------------+
                   |                             |
             [Passes]                        [Fails]
                   |                             |
                   v                             v
     +-------------------------------+   +-----------------------+
     |  bot/client.py Initialization |   | Print Validation Error|
     +-------------------------------+   |       and Exit        |
                   |                     +-----------------------+
        +----------+----------+
        |                     |
     [Keys Set]         [Keys Unset]
        |                     |
        v                     v
+----------------------+   +------------------------------------+
|    Live REST Mode    |   |       Demo / Simulation Mode       |
|  - Real Client Init  |   |  - Simulated Client Init           |
|  - Real Ping Handshake|  |  - Bypasses ping check             |
+----------------------+   +------------------------------------+
        |                     |
        +----------+----------+
                   |
                   v
     +-------------------------------+
     |   bot/orders.py order execution|
     |   (Bypasses live API in demo)  |
     +-------------------------------+
                   |
                   v
     +-------------------------------+
     | Format and Log receipt details|
     |   to logs/trading_bot.log     |
     +-------------------------------+
                   |
                   v
     +-------------------------------+
     |  Print Styled Receipt Panel   |
     |          to Terminal          |
     +-------------------------------+
```

---

## 🛠️ Project Structure
```
.git/
bot/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Binance Futures testnet client initialization wrapper
│   ├── orders.py            # Market and Limit order placement and parsing logic
│   ├── validators.py        # Pure-Python strict CLI input validator
│   └── logging_config.py    # Rotating file logging setup
│
├── logs/
│   └── trading_bot.log      # Active log file (contains simulated run logs)
│
├── cli.py                   # Main CLI Entry Point (Argparse + Enhanced Interactive UX)
├── requirements.txt         # Project package dependencies
├── .env.template            # API credentials template env file
├── .gitignore               # Excludes virtual environments, credentials
└── README.md                # Documentation manual
```

---

## 🚀 Setup Instructions

### 1. Prerequisite
Ensure you have **Python 3.8+** installed on your machine.

### 2. Install Dependencies
Install the required python libraries directly in your terminal:
```bash
pip install -r requirements.txt
```

### 3. Generate and Configure API Keys (Optional)
If you wish to make live trades on the real Binance exchange:
1. Go to the [Binance Futures Testnet Portal](https://testnet.binancefuture.com), register/login, and generate a new **API Key** and **Secret Key**.
2. Create a file named `.env` in the root directory (adjacent to `cli.py`):
```bash
cp .env.template .env
```
3. Open `.env` and fill in your generated credentials:
```env
BINANCE_API_KEY=your_actual_binance_testnet_api_key
BINANCE_API_SECRET=your_actual_binance_testnet_api_secret
```
*Note: If no `.env` file exists or keys are empty, the bot automatically falls back to **Demo Mode**.*

---

## 🖥️ How to Run & Examples

### Option A: Enhanced Interactive UX (Recommended Bonus Option)
Simply run the script with **no arguments** to launch the gorgeous interactive terminal guide:
```bash
python cli.py
```
This guides you step-by-step:
1. Enter your symbol (e.g., `BTCUSDT`).
2. Select your side (`BUY` / `SELL`) using interactive options.
3. Select your order type (`MARKET` / `LIMIT`) using interactive options.
4. Input quantity.
5. Input price (only requested if `LIMIT` is selected).
6. Confirms order placement with a styled summary card and table before submitting!

---

### Option B: Argparse Automated Mode
Provide command-line flags to immediately run a specific order:

#### 1. Place a MARKET BUY Order:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

#### 2. Place a LIMIT SELL Order:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 68500.5
```

---

## 📝 Logging and Diagnostics
- Detailed logs of API requests, parameters, server ping health, raw JSON responses, and exceptions are saved in:
  `logs/trading_bot.log`
- Logging features automatic rotation (10MB maximum size with 5 backup files) to prevent high disk usage.

---

## 💡 Assumptions and Architecture Decisions
- **USDT-M Futures Contract Spec**: We target USDT-Margined futures contract orders only. For LIMIT orders, we default the `timeInForce` value to `'GTC'` (Good 'Til Cancelled) which is a mandatory requirement by Binance's matching engine.
- **Client Connectivity Ping**: During client initialization in `bot/client.py`, the wrapper performs an initial `futures_ping()` to ensure API connection and credentials are valid before letting the order proceed.
- **Environment Isolation**: We restrict logging and credentials to local untracked files (`.env`, `logs/`) keeping production repositories completely secure and clean.
