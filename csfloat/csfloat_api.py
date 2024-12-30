import logging
from csfloat.rest_client import RestClient
from csfloat.exceptions import CSFloatApiException
from csfloat.models import BuyOrder
from typing import List,Dict

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


    def get_our_buy_orders(self) -> List[BuyOrder]:
        """Returns our current active buy orderes on csfloat 

        Returns:
            List[BuyOrder]: Returns a list of buy order objects. 
        """
        endpoint = "/v1/me/buy-orders"
        orders = self._page(endpoint=endpoint)

        
        return [BuyOrder(**order) for order in orders]
        
    def get_item_buy_orders(self,listing_id: str) -> List[BuyOrder]:
        """Get a list of the top buy orders for a given listing ID on csfloat.
           a listing ID has to be used to fetch the data, even though all buy order data is the same for a given market hash name
           

        Args:
            listing_id (str): requires a csfloat listing ID, buy order ID can't be used 

        Returns:
            List[BuyOrder]: Returns a list of buy order objects. 
        """

        pass
    
    def create_buy_order(self):
        pass
    def remove_buy_order(self):
        pass
    def get_listings_from_market_hash(self,market_hash: str,limit: int = 1,sort_by: str = "lowest_price",type: str = "buy_now") -> List: #list[Listing]
        endpoint = "/v1/listings"
        params = {"market_hash_name" : market_hash, "limit" : limit, sort_by : sort_by, type: type}
        result = self._rest_adapter.get(endpoint=endpoint,ep_params=params)
        return result.data

    def get_balance(self):
        pass

