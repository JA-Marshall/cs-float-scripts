from csfloat.csfloat_api import CSFloatApi
from csfloat.models import *
from dotenv import load_dotenv
import os
import logging
import pprint


def main() -> None:
    logger = configure_logging()
    api_key : str = load_api_key()
    csfloat = CSFloatApi(api_key=api_key,logger=logger)
    # buy_orders = csfloat.get_our_buy_orders()
    
    # listings = csfloat.get_listings_from_market_hash(market_hash="Gamma Case")
    # for listing in listings:
    #     print(listing)
    market_hash_name,max_price,quantity = "Prisma 2 Case",50,50
    csfloat.create_buy_order(market_hash_name=market_hash_name,max_price=max_price,quantity=quantity)



def load_api_key() -> str:
    
    load_dotenv('.env')
    api_key = os.getenv('CS_FLOAT_API_KEY')
    return api_key

def configure_logging() -> logging.Logger:
   
    logger = logging.getLogger("CSFloat-logger")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


if __name__ == '__main__':
    main()