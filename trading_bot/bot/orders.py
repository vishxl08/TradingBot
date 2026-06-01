import logging
from typing import Dict, Any, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)

def place_futures_order(
    client: Client, 
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Places a MARKET or LIMIT order on the Binance Futures Testnet (USDT-M).
    Handles logging of request, response, and error details.
    
    Returns:
        A dictionary containing structured success details or raises an exception on failure.
    """
    # 1. Structure the request parameters
    params: Dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }
    
    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  # Good 'Til Cancelled - standard for Binance LIMIT orders
        
    logger.info("PRE-ORDER REQUEST SUMMARY:")
    logger.info("  Symbol: %s", symbol)
    logger.info("  Side: %s", side)
    logger.info("  Type: %s", order_type)
    logger.info("  Quantity: %s", quantity)
    if price:
        logger.info("  Price: %s", price)
    logger.info("Full request payload: %s", params)

    try:
        # 2. Place order via python-binance futures endpoint
        logger.info("Sending order placement request to Binance Futures API...")
        response = client.futures_create_order(**params)
        
        # 3. Log the successful response
        logger.info("POST-ORDER RESPONSE RECEIVED:")
        logger.info("Raw API Response: %s", response)
        
        # Extract crucial details
        order_id = response.get("orderId")
        status = response.get("status")
        executed_qty = response.get("executedQty", "0.0")
        
        # In Futures, average price might be in 'avgPrice'
        avg_price = response.get("avgPrice")
        if not avg_price or float(avg_price) == 0.0:
            # Fallback if average price is not populated immediately for LIMIT
            avg_price = response.get("price", "0.0")
            
        logger.info("Parsed response details -> OrderId: %s, Status: %s, ExecutedQty: %s, AvgPrice: %s", 
                    order_id, status, executed_qty, avg_price)
                    
        return {
            "success": True,
            "orderId": order_id,
            "status": status,
            "executedQty": executed_qty,
            "avgPrice": avg_price,
            "symbol": response.get("symbol"),
            "side": response.get("side"),
            "type": response.get("type"),
            "raw": response
        }

    except BinanceAPIException as e:
        # Log the specific API error from Binance (e.g., balance insufficient, invalid precision, etc.)
        error_msg = f"Binance Futures API Error: {e.message} (Code: {e.code}, Status Code: {e.status_code})"
        logger.error("Failed to place order. %s", error_msg)
        logger.error("Error raw details: %s", str(e))
        return {
            "success": False,
            "error_type": "BinanceAPIException",
            "message": e.message,
            "code": e.code,
            "status_code": e.status_code,
            "raw": str(e)
        }
        
    except BinanceRequestException as e:
        # Log request issue (e.g. malformed JSON, network error before reaching Binance)
        error_msg = f"Binance Request Error: {str(e)}"
        logger.error("Failed to place order. %s", error_msg)
        return {
            "success": False,
            "error_type": "BinanceRequestException",
            "message": str(e),
            "raw": str(e)
        }
        
    except Exception as e:
        # Log any other unexpected exception (e.g., connection timed out, dns failure)
        error_msg = f"Unexpected Error: {str(e)}"
        logger.exception("Failed to place order due to an unexpected error.")
        return {
            "success": False,
            "error_type": "UnexpectedException",
            "message": str(e),
            "raw": str(e)
        }
