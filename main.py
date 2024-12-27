import requests
import pprint
import json
from dotenv import load_dotenv
import os
import logging
from typing import Dict,Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point"""
    #### temp id for testing
    listing_id = 791974964206110791
    try:
        headers = build_headers()
        highest_order = get_item_buy_order_from_listing_id(listing_id, headers)
        logger.info(f"Highest buy order: {highest_order}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def build_headers() -> Dict[str, str]:
    """
    Build headers for the API request using the API key from .env.

    Returns:
        Dict[str, str]: Headers for the API request.
    Raises:
        ValueError: If the API key is not found in the environment.
    """
     
    load_dotenv('.env')
    api_key = os.getenv('CS_FLOAT_API_KEY')
    if not api_key:
        logger.error("API key not found. Please check your .env file.")
        raise ValueError("API key not found in environment variables.")
    return {'Authorization': api_key}


def get_item_buy_order_from_listing_id(listing_id: int, headers: Dict[str, str]) -> Tuple[str, int]:

    """
    Fetch the highest buy order for a given listing ID.

    Args:
        listing_id (int): The ID of the listing to query.
        headers (Dict[str, str]): Headers for the API request.

    Returns:
        Tuple[str, int]: The highest buy order price and quantity.

    Raises:
        Exception: If the API request fails or returns a non-200 status code.
    """
    url = f'https://csfloat.com/api/v1/listings/{listing_id}/buy-orders?limit=10'
    logger.debug(f"Making GET request to URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"API request failed with status code {response.status_code}.")
        raise Exception(f"Failed to fetch data: HTTP {response.status_code}")
    
    data = response.json()  # Use `json()` directly instead of `json.loads(response.content)`
    if not data or not isinstance(data, list) or not data[0]:
        logger.error("Unexpected or empty response format.")
        raise ValueError("Invalid data received from API.")
    
    highest_order = (f"${data[0]['price'] / 100:.2f}", data[0]['qty'])
    logger.info(f"Fetched highest order: {highest_order}")
    return highest_order

if __name__ == '__main__':
    main()