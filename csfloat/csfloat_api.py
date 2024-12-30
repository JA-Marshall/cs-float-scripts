import logging
from csfloat.rest_client import RestClient
from csfloat.exceptions import CSFloatApiException
from csfloat.models import BuyOrder
from typing import List,Dict

class CSFloatApi:
    def __init__(self, api_key: str,logger: logging.Logger = None,hostname:str='csfloat.com/api'):
        self._rest_adapter = RestClient(hostname, api_key, logger)
    
    #assuming this is 100 for most things, but will change if its not 
    def _page(self,  endpoint:str,items_per_page: str = 100,) -> List[Dict]:
        pass


    def get_our_buy_orders(self) -> List[BuyOrder]:
        """Returns our current active buy orderes on csfloat 

        Returns:
            List[BuyOrder]: Returns a list of buy order objects. 
        """
        endpoint = "/v1/me/buy-orders"
        result = self._rest_adapter.get(endpoint=f'{endpoint}?page=0&limit=100')
        count = result.data['count']
        if count <= 100:
            buy_orders = [BuyOrder(**order) for order in result.data['orders']]
            return buy_orders
        self._page()
    
    def get_item_buy_orders(self,listing_id: str) -> List[BuyOrder]:
        """Get a list of the top buy orders for a given item on csfloat.

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
    
    def get_balance(self):
        pass

