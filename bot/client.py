import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# Load local environment variables from a .env file if it exists
load_dotenv()

logger = logging.getLogger(__name__)

def get_binance_client() -> Client:
    """
    Initializes and returns a python-binance Client configured for the Binance Futures Testnet.
    Credentials are loaded securely from environment variables.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    # We validate presence of keys. If missing, we explain clearly how to obtain/set them.
    if not api_key or not api_secret:
        error_msg = (
            "Binance Futures Testnet API credentials not found in environment variables.\n"
            "Please create a '.env' file in the root of the project or set the environment variables:\n"
            "  export BINANCE_API_KEY='your_api_key'\n"
            "  export BINANCE_API_SECRET='your_api_secret'\n"
            "You can generate testnet keys at: https://testnet.binancefuture.com"
        )
        logger.error("API credentials missing: BINANCE_API_KEY or BINANCE_API_SECRET is unset.")
        raise ValueError(error_msg)
        
    logger.info("Initializing Binance Client for Futures Testnet (https://testnet.binancefuture.com)...")
    
    try:
        # testnet=True tells the client to use testnet base URLs.
        # For spot: testnet.binance.vision
        # For futures: testnet.binancefuture.com
        client = Client(api_key=api_key, api_secret=api_secret, testnet=True)
        
        # Verify the client connectivity by making a simple request to futures_ping()
        logger.info("Testing connectivity to Binance Futures Testnet via futures_ping()...")
        client.futures_ping()
        logger.info("Connectivity check passed. Successfully connected to Futures Testnet.")
        
        return client
        
    except BinanceAPIException as e:
        logger.exception("Binance API Exception during client initialization: %s", e)
        raise RuntimeError(f"Failed to connect to Binance API: {e.message} (Code: {e.code})") from e
    except Exception as e:
        logger.exception("Unexpected error during client initialization: %s", e)
        raise RuntimeError(f"An unexpected connection error occurred: {str(e)}") from e
