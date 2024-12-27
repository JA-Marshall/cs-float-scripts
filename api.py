import requests
from typing import Dict, Tuple, List
from dotenv import load_dotenv
import os

def build_headers() -> Dict[str, str]:
    """
    Build headers for the API request using the API key from .env.

    Returns:
        Dict[str, str]: Headers for the API request.
    """
    load_dotenv('.env')
    api_key = os.getenv('CS_FLOAT_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please check your .env file.")
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
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  

    data = response.json()
    if not data or not isinstance(data, list):
        raise ValueError("Invalid or empty response received from API.")

    highest_order = data[0]
    if not all(key in highest_order for key in ['price', 'qty']):
        raise ValueError("Response data is missing required fields.")

    return (f"${highest_order['price'] / 100:.2f}", highest_order['qty'])

def get_our_current_buy_orders(headers: Dict[str, str]) -> List[Dict[str, str | float | int]]:
    """
    Fetch all of our current buy orders on csfloat

    Args:
        headers (Dict[str, str]): Headers for the API request.

    Returns:
        List[Dict[str, str | float | int]
        returns a list of dicts with the item name, quantity and price.
    """
    url = "https://csfloat.com/api/v1/me/buy-orders?page=0&limit=10&order=desc"
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    

    buy_orders = []
    for order in data.get("orders", []):
        buy_orders.append({
            # "created_at": order["created_at"],
            "item_name": order["market_hash_name"],
            "quantity": order["qty"],
            "price": order["price"] / 100.0,  # Convert from cents to dollars
        })
    print(buy_orders)
    return buy_orders
