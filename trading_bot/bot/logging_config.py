import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_dir: str = "logs", log_file: str = "trading_bot.log", level: int = logging.INFO):
    """
    Sets up structured logging to both a file (with rotation) and the console.
    Ensures that the log directory exists.
    """
    # Build absolute path or path relative to the script execution dir
    # To keep things clean, we will create the log directory in the current working directory.
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        
    log_path = os.path.join(log_dir, log_file)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers if any to prevent duplicate logging
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            
    # File handler (logs detailed request/response details, rotates at 10MB)
    file_formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] (%(name)s) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler = RotatingFileHandler(log_path, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)
    root_logger.addHandler(file_handler)
    
    # Console handler (for a clean user output, handled visually in cli.py using Rich)
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.WARNING)  # Only warnings/errors in console, Rich will handle normal info output
    root_logger.addHandler(console_handler)
    
    logging.info("Logging configured successfully. Log file path: %s", os.path.abspath(log_path))
    return root_logger
