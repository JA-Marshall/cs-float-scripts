from typing import List,Dict,Optional
from dataclasses import dataclass

from pydantic import BaseModel



@dataclass
class Result:
    """
    Result returned from low-level RestClient
    :param status_code: Standard HTTP Status code
    :param message: Human readable result
    :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
    """
    status_code: int
    message: str = ''
    data: Optional[List[Dict]] = None


class BuyOrder(BaseModel):
    """
    Data structure representing a buy order on csfloat
    :param id: ID for a given buy order
    :param created_at: Date when the buy order was created
    :param market_hash_name: Name for a given item on csfloat
    :param qty: Quantity the buy order is for 
    :param price: Bid price of the buy order 
    """
    id: str
    created_at: str
    market_hash_name: str
    qty: int
    price: int

class Item(BaseModel):
    """
    Represents an item in a marketplace listing.

    Attributes:
        market_hash_name (str): The market hash name of the item, used to identify it uniquely in the marketplace.
        is_commodity (bool): Indicates whether the item is a commodity (true if all instances of the item are identical).
        type_name (str): The category or type of the item (e.g., "Container").
    """
    market_hash_name: str
    is_commodity: bool
    type_name: str


class Listing(BaseModel):
    """
    Represents a listing in the marketplace.

    Attributes:
        created_at (str): The timestamp when the listing was created, in ISO 8601 format.
        type (str): The type of listing (e.g., "buy_now").
        id (str): The unique identifier for the listing.
        price (int): The price of the listing, typically in the smallest currency unit (e.g., cents).
        market_hash_name (str): The market hash name of the item being listed.
        is_commodity (bool): Indicates whether the listed item is a commodity (true if all instances of the item are identical).
        type_name (str): The category or type of the listed item (e.g., "Container").
    """
    created_at: str
    type: str
    id: str
    price: int
    market_hash_name: str
    is_commodity: bool
    type_name: str

