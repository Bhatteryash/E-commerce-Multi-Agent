import logging
import sys
from typing import Optional

def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name (str): The name of the logger
        level (Optional[int]): The logging level. Defaults to INFO if not specified.
        
    Returns:
        logging.Logger: The configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Set level (default to INFO if not specified)
    logger.setLevel(level or logging.INFO)
    
    # Only add handler if logger doesn't already have handlers
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level or logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger 