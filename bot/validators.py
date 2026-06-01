import re
from typing import Dict, Any, Tuple, Optional

def validate_inputs(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: str, 
    price: Optional[str] = None
) -> Tuple[bool, Optional[str], Dict[str, Any]]:
    """
    Validates the 5 CLI arguments for the trading bot.
    Returns:
        (is_valid, error_message, validated_parameters_dict)
    """
    validated_params = {}
    
    # 1. Validate Symbol
    if not symbol:
        return False, "Symbol is required.", {}
    
    symbol_clean = str(symbol).strip().upper()
    # Simple regex to check Binance futures-like symbols (e.g. BTCUSDT, ETHUSDT)
    # They should be alphanumeric, between 3 to 15 chars.
    if not re.match(r"^[A-Z0-9]{3,15}$", symbol_clean):
        return False, f"Invalid symbol format: '{symbol}'. Must be alphanumeric and 3-15 characters long.", {}
    
    validated_params['symbol'] = symbol_clean
    
    # 2. Validate Side
    if not side:
        return False, "Order side is required.", {}
    
    side_clean = str(side).strip().upper()
    if side_clean not in ("BUY", "SELL"):
        return False, f"Invalid order side: '{side}'. Must be either 'BUY' or 'SELL'.", {}
    
    validated_params['side'] = side_clean
    
    # 3. Validate Order Type
    if not order_type:
        return False, "Order type is required.", {}
        
    type_clean = str(order_type).strip().upper()
    if type_clean not in ("MARKET", "LIMIT"):
        return False, f"Invalid order type: '{order_type}'. Must be either 'MARKET' or 'LIMIT'.", {}
        
    validated_params['order_type'] = type_clean
    
    # 4. Validate Quantity
    if not quantity:
        return False, "Quantity is required.", {}
        
    try:
        qty_val = float(quantity)
        if qty_val <= 0:
            return False, f"Quantity must be a positive number. Got: {quantity}", {}
    except ValueError:
        return False, f"Quantity must be a valid numeric value. Got: '{quantity}'", {}
        
    validated_params['quantity'] = qty_val
    
    # 5. Validate Price
    price_val = None
    if type_clean == "LIMIT":
        if not price:
            return False, "Price is required for LIMIT orders.", {}
        try:
            price_val = float(price)
            if price_val <= 0:
                return False, f"Price must be a positive number. Got: {price}", {}
        except ValueError:
            return False, f"Price must be a valid numeric value. Got: '{price}'", {}
    else:
        # For MARKET orders, price is not required. If provided, we ignore it or set it to None.
        if price:
            try:
                # Still check if it's numeric if they passed it, just in case
                float(price)
            except ValueError:
                return False, f"Warning/Error: Provided price '{price}' is not a valid numeric value.", {}
                
    validated_params['price'] = price_val
    
    return True, None, validated_params
