import logging
from csfloat.rest_client import RestClient
from csfloat.exceptions import CSFloatApiException
from csfloat.models import OurBuyOrder,MarketBuyOrder,Listing
from typing import List,Dict
import pprint

class CSFloatApi:
    def __init__(self, api_key: str,logger: logging.Logger = None,hostname:str='csfloat.com/api'):
        self._rest_adapter = RestClient(hostname, api_key, logger)
    
    def _page(self, endpoint: str, items_per_page: int = 100) -> List[Dict]:

        """
        Pagination function to retrieve all items from an endpoint.

        Args:
            endpoint (str):  endpoint to fetch data from.
            items_per_page (int): Number of items per page, defaulted to 100

        Returns:
            List[Dict]: List of all items retrieved from the endpoint.
        """
        
        result = self._rest_adapter.get(endpoint=endpoint,ep_params={'page': 0, 'limit' : items_per_page})
        total_count = result.data['count']
        all_data = result.data['orders']

        
        total_pages = total_count // items_per_page
        if total_count % items_per_page != 0:
            total_pages += 1

       
        for page in range(1, total_pages):
            result = self._rest_adapter.get(endpoint=endpoint,params={'page': page, 'limit' : items_per_page})
            all_data.extend(result.data['orders'])
            
        return all_data

    #undoccumented api
    def get_our_buy_orders(self) -> List[OurBuyOrder]:
        """Returns our current active buy orderes on csfloat 

        Returns:
            List[OurBuyOrder]: Returns a list of buy order objects. 
        """
        endpoint = "/v1/me/buy-orders"
        orders = self._page(endpoint=endpoint)

        
        return [OurBuyOrder(**order) for order in orders]
    
    #undoccumented api
    def get_item_buy_orders(self,listing_id: str) -> List[MarketBuyOrder]:
        """Get a list of the top buy orders for a given listing ID on csfloat.
           a listing ID has to be used to fetch the data, even though all buy order data is the same for a given market hash name
           

        Args:
            listing_id (str): requires a csfloat listing ID, buy order ID can't be used 

        Returns:
            List[MarketBuyOrder]: Returns a list of buy order objects. 
        """
        endpoint = f'/v1/listings/{listing_id}/buy-orders?limit=10'
        result = self._rest_adapter.get(endpoint=endpoint)
        
        #Get rid of all buy orders with specific float/condition requirements,
        #not an ideal solution 
        filtered_data = [order for order in result.data if "expression" not in order]
        return [MarketBuyOrder(**order) for order in filtered_data]

        

    def create_buy_order(self,market_hash_name : str, max_price: str, quantity: str)-> bool:
        """Create a buy order on csfloat, 

        Args:
            market_hash_name (str): market hash name for the item we want to place a buy order
            max_price (str): price for the item IN CENTS, $0.50 == 50, $19.99 = 1999
            quantity (str): The quantity of items you want the buy order to be for

        Returns:
            bool: Returns True/False depending on if we sucessfully place the order
        """
        endpoint = '/v1/buy-orders'
        data = {'market_hash_name' : market_hash_name,
                  'max_price': max_price,
                  'quantity' : quantity}
        
        result = self._rest_adapter.post(endpoint=endpoint,data=data)
    
        if result.status_code == 200:
            return True
        return False
    
    def remove_buy_order(self,id : str) -> bool:
        """Remove a buy order from csfloat

        Args:
            id (str): ID of a buy order on csfloat

        Returns:
            bool: Returns True or False if the request was successful 
        """

        endpoint = f'/v1/buy-orders/{id}'
        result = self._rest_adapter.delete(endpoint=endpoint)
        if result.status_code == 200:
            return True
        return False

        
    def get_listings_from_market_hash(self,market_hash: str,limit: int = 1,sort_by: str = "lowest_price",type: str = "buy_now") -> List[Listing]:
        """Get listings on csfloat given a specific market hash
        https://docs.csfloat.com/#introduction

        Args:
            market_hash (str): An item market hash on CS Float
            limit (int, optional): The amount of listings to fetch, Defaulted to 1 
            sort_by (str, optional): The sorting of listings Defaults to "lowest_price".
            type (str, optional): Listing type Defaults to "buy_now".

        Returns:
            List[Listing]: Returns a List containing Listing objects with data about the listing
        """
        endpoint = "/v1/listings"
        params = {"market_hash_name" : market_hash, "limit" : limit, sort_by : sort_by, type: type}
        result = self._rest_adapter.get(endpoint=endpoint,ep_params=params)
        
        data = result.data['data']
        listings = []
        for item in data:
            flattened_data = {**item, **item.pop("item", {})}  # Flatten 'item' fields into the main dictionary
            listings.append(Listing(**flattened_data))  
        
        return listings
        

    def get_balance(self) -> int:
        """get our current balance on csfloat

        Returns:
            int: returns an int representing our balance on csfloat
        """
        endpoint = "/v1/me"
        result = self._rest_adapter.get(endpoint=endpoint)
        data = result.data['user']
        balance = data['balance']
        
        return balance

