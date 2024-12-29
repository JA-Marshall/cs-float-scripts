import logging
from csfloat.rest_client import RestClient
from csfloat.exceptions import CSFloatApiException
from csfloat.models import *

class CSFloatApi:
    def __init__(self, api_key: str,logger: logging.Logger = None,hostname:str='csfloat.com/api'):
        self._rest_adapter = RestClient(hostname, api_key, logger)
    
    def get_our_buy_orders(self) -> List[BuyOrder]:
        result = self._rest_adapter.get(endpoint='/v1/me/buy-orders?page=0&limit=10&order=desc')
        buy_orders = [BuyOrder(**order) for order in result.data['orders']]
        return buy_orders