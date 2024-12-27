import requests
from typing import Dict, Tuple, List, Union
from dotenv import load_dotenv
import os
from logger import log_to_console

def build_headers() -> Dict[str, str]:
    """
    Build headers for the API request using the API key from .env.

    Returns:
        Dict[str, str]: Headers for the API request.
    """
    log_to_console("Building headers for the API request...", level="info")
    load_dotenv('.env')
    api_key = os.getenv('CS_FLOAT_API_KEY')
    if not api_key:
        error_message = "API key not found. Please check your .env file."
        log_to_console(error_message, level="error")
        raise ValueError(error_message)
    return {'Authorization': api_key}


def fetch_highest_buy_order(listing_id: int, headers: Dict[str, str]) -> Tuple[str, int]:
    """
    Fetch the highest buy order for a given listing ID.

    Args:
        listing_id (int): The ID of the listing to query.
        headers (Dict[str, str]): Headers for the API request.

    Returns:
        Tuple[str, int]: The highest buy order price and quantity.
    """
    url = f"https://csfloat.com/api/v1/listings/{listing_id}/buy-orders?limit=10"
    log_to_console(f"Fetching highest buy order for listing ID: {listing_id}", level="info")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        log_to_console(f"API call successful for listing ID: {listing_id}", level="info")
    except requests.exceptions.RequestException as e:
        log_to_console(f"API request failed for listing ID {listing_id}: {e}", level="error")
        raise RuntimeError(f"API request failed: {e}")
    
    data = response.json()
    if not data or not isinstance(data, list):
        error_message = "Invalid or empty response received from API."
        log_to_console(error_message, level="warning")
        raise ValueError(error_message)

    highest_order = data[0]
    if not all(key in highest_order for key in ['price', 'qty']):
        error_message = "Response data is missing required fields."
        log_to_console(error_message, level="warning")
        raise ValueError(error_message)

    return (f"${highest_order['price'] / 100:.2f}", highest_order['qty'])


def get_our_current_buy_orders(headers: Dict[str, str]) -> List[Dict[str, Union[str, float, int]]]:
    """
    Fetch all of our current buy orders on csfloat.

    Args:
        headers (Dict[str, str]): Headers for the API request.

    Returns:
        List[Dict[str, Union[str, float, int]]]: List of buy orders with item name, quantity, and price.
    """
    url = "https://csfloat.com/api/v1/me/buy-orders?page=0&limit=10&order=desc"
    log_to_console("Fetching current buy orders...", level="info")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        log_to_console("Successfully fetched current buy orders.", level="info")
    except requests.exceptions.RequestException as e:
        log_to_console(f"Failed to fetch buy orders: {e}", level="error")
        raise RuntimeError(f"API request failed: {e}")

    data = response.json()
    buy_orders = []
    for order in data.get("orders", []):
        buy_orders.append({
            "market_hash_name": order["market_hash_name"],
            "quantity": order["qty"],
            "price": order["price"] / 100.0,  # Convert from cents to dollars
        })

    log_to_console(f"Parsed {len(buy_orders)} buy orders.", level="info")
    return buy_orders

def get_listing_id_from_market_hash(headers : Dict[str,str],market_hash: str) -> str:
    """Query the csfloat API with a market hash, then get the instance id of the first listing.
    This instance id is used for getting the buy order list for the given item
    
    Args:
        headers (Dict[str, str]): Headers for the API request.
        market_hash  str : market_hash for an item on cs float
    Returns:
        str  : returns a listing instance ID 
    """
    url = "https://csfloat.com/api/v1/listings"
    params = {"market_hash_name" : market_hash}

    log_to_console(f"Fetching listing ID for {market_hash}...", level="info")
    try:
        response = requests.get(url, headers=headers,params=params, timeout=10)
        response.raise_for_status()
        log_to_console("Successfully fetched current buy orders.", level="info")
    except requests.exceptions.RequestException as e:
        log_to_console(f"Failed to fetch buy orders: {e}", level="error")
        raise RuntimeError(f"API request failed: {e}")
    print(response.content)
    #TODO
    return response.json