from csfloat.csfloat_api import CSFloatApi
from csfloat.models import *
from dotenv import load_dotenv
import os

def main() -> None:
    api_key : str = load_api_key()
    csfloat = CSFloatApi(api_key=api_key)
    result = csfloat.get_buy_orders()
    print(result.data)

def load_api_key() -> str:
    load_dotenv('.env')
    api_key = os.getenv('CS_FLOAT_API_KEY')
    return api_key

if __name__ == '__main__':
    main()