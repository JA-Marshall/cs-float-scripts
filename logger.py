import logging
import requests
from typing import Optional


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# DISCORD_WEBHOOK_URL = "your_discord_webhook_url"  

def log_to_console(message: str, level: str = "info") -> None:
    """
    Log a message to the console.

    Args:
        message (str): The message to log.
        level (str): The logging level ('info', 'warning', 'error', etc.).
    """
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    else:
        logger.debug(message)

##TODO
def log_to_discord(message: str) -> Optional[bool]:
    """
    NOT WRITTEN YET
    Send a log message to Discord via a webhook.
    """
    pass
    
    
  
