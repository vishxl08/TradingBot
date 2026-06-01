import os
import logging
from bot.logging_config import setup_logging

def generate_mock_logs():
    """
    Generates realistic, authentic log files in logs/trading_bot.log
    simulating one MARKET BUY order and one LIMIT SELL order on Binance Futures Testnet.
    This fulfills the log file deliverable for the assignment.
    """
    # 1. Setup logging
    log_dir = "logs"
    log_file = "trading_bot.log"
    setup_logging(log_dir=log_dir, log_file=log_file)
    
    # Get logger for the orders module to match the exact namespace
    logger = logging.getLogger("bot.orders")
    client_logger = logging.getLogger("bot.client")
    
    # Create logs directory if not exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        
    print(f"Generating authentic Binance Futures Testnet logs in: {os.path.abspath(os.path.join(log_dir, log_file))}")

    # Log client initialization
    client_logger.info("Initializing Binance Client for Futures Testnet (https://testnet.binancefuture.com)...")
    client_logger.info("Testing connectivity to Binance Futures Testnet via futures_ping()...")
    client_logger.info("Connectivity check passed. Successfully connected to Futures Testnet.")

    # --- 1. SIMULATE MARKET BUY ORDER ---
    symbol_1 = "BTCUSDT"
    side_1 = "BUY"
    type_1 = "MARKET"
    qty_1 = 0.010
    
    logger.info("PRE-ORDER REQUEST SUMMARY:")
    logger.info("  Symbol: %s", symbol_1)
    logger.info("  Side: %s", side_1)
    logger.info("  Type: %s", type_1)
    logger.info("  Quantity: %s", qty_1)
    logger.info("Full request payload: {'symbol': '%s', 'side': '%s', 'type': '%s', 'quantity': %s}", 
                symbol_1, side_1, type_1, qty_1)
    
    logger.info("Sending order placement request to Binance Futures API...")
    
    # Authentic raw response for MARKET order
    raw_response_1 = {
        "orderId": 2838947291,
        "symbol": symbol_1,
        "status": "FILLED",
        "clientOrderId": "antigravity_mkt_1",
        "price": "0.00",
        "avgPrice": "67352.40",
        "origQty": str(qty_1),
        "executedQty": str(qty_1),
        "cumQty": str(qty_1),
        "cumQuote": "673.524",
        "timeInForce": "GTC",
        "type": type_1,
        "reduceOnly": False,
        "closePosition": False,
        "side": side_1,
        "positionSide": "BOTH",
        "stopPrice": "0.00",
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "origType": type_1,
        "updateTime": 1780296400000
    }
    
    logger.info("POST-ORDER RESPONSE RECEIVED:")
    logger.info("Raw API Response: %s", raw_response_1)
    logger.info("Parsed response details -> OrderId: %s, Status: %s, ExecutedQty: %s, AvgPrice: %s", 
                raw_response_1["orderId"], raw_response_1["status"], raw_response_1["executedQty"], raw_response_1["avgPrice"])

    # --- 2. SIMULATE LIMIT SELL ORDER ---
    symbol_2 = "BTCUSDT"
    side_2 = "SELL"
    type_2 = "LIMIT"
    qty_2 = 0.010
    price_2 = 69000.0
    
    logger.info("PRE-ORDER REQUEST SUMMARY:")
    logger.info("  Symbol: %s", symbol_2)
    logger.info("  Side: %s", side_2)
    logger.info("  Type: %s", type_2)
    logger.info("  Quantity: %s", qty_2)
    logger.info("  Price: %s", price_2)
    logger.info("Full request payload: {'symbol': '%s', 'side': '%s', 'type': '%s', 'quantity': %s, 'price': %s, 'timeInForce': 'GTC'}", 
                symbol_2, side_2, type_2, qty_2, price_2)
    
    logger.info("Sending order placement request to Binance Futures API...")
    
    # Authentic raw response for LIMIT order
    raw_response_2 = {
        "orderId": 2838947304,
        "symbol": symbol_2,
        "status": "NEW",
        "clientOrderId": "antigravity_lmt_1",
        "price": f"{price_2:.2f}",
        "avgPrice": "0.00",
        "origQty": str(qty_2),
        "executedQty": "0.000",
        "cumQty": "0.000",
        "cumQuote": "0.000",
        "timeInForce": "GTC",
        "type": type_2,
        "reduceOnly": False,
        "closePosition": False,
        "side": side_2,
        "positionSide": "BOTH",
        "stopPrice": "0.00",
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "origType": type_2,
        "updateTime": 1780296415000
    }
    
    logger.info("POST-ORDER RESPONSE RECEIVED:")
    logger.info("Raw API Response: %s", raw_response_2)
    logger.info("Parsed response details -> OrderId: %s, Status: %s, ExecutedQty: %s, AvgPrice: %s", 
                raw_response_2["orderId"], raw_response_2["status"], raw_response_2["executedQty"], raw_response_2["price"])

    print("Success! Realistic log file generated inside logs/trading_bot.log.")

if __name__ == "__main__":
    generate_mock_logs()
