from typing import List,Dict,Optional
from dataclasses import dataclass

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

@dataclass
class BuyOrder:
    """
    Data strucutre representing a buy order on csfloat
    :param id: id for a given buy order
    :param created_at: Date when the buy order was created
    :param market_hash_name: name for a given item on csfloat
    :param qty: quantity the buy order is for 
    :param price: bid price of the buy order 
    """
    id: str
    created_at: str
    market_hash_name: str
    qty: int
    price: int