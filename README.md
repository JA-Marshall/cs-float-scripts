﻿# cs-float-scripts
# cs-float-scripts
This is a Python wrapper for interacting with the CSFloat API. It allows you to create, view, and manage buy orders, as well as retrieve item listings and your current active buy orders.


Example Code: 
```python3
from csfloat_api import CSFloatApi
import os
from dotenv import load_dotenv

def main():
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("CS_FLOAT_API_KEY")

    # Initialize the CSFloat API
    csfloat = CSFloatApi(api_key)

    # Example: Create a buy order
    market_hash_name = "Prisma 2 Case"
    max_price = 50  # Price in cents ($0.50 = 50)
    quantity = 10   # Number of items
    success = csfloat.create_buy_order(market_hash_name, max_price, quantity)

    if success:
        print(f"Successfully created a buy order for {quantity} '{market_hash_name}' at {max_price} cents each.")
    else:
        print("Failed to create a buy order.")

    # Example: Get all active buy orders
    buy_orders = csfloat.get_our_buy_orders()
    for order in buy_orders:
        print(f"Buy Order ID: {order.id}, Item: {order.market_hash_name}, Price: {order.price}, Quantity: {order.quantity}")

    # Example: Remove a buy order by ID
    if buy_orders:
        first_order_id = buy_orders[0].id
        removed = csfloat.remove_buy_order(first_order_id)
        if removed:
            print(f"Successfully removed buy order with ID: {first_order_id}")
        else:
            print(f"Failed to remove buy order with ID: {first_order_id}")

if __name__ == "__main__":
    main()```
