# CSFloat Buy Order Manager

A Python wrapper for interacting with the CSFloat API. This library provides an easy-to-use interface for creating, viewing, and managing buy orders on CSFloat, as well as retrieving item listings and market data.

**⚠️ Important Note:** CSFloat's API is largely undocumented. This library is based on reverse engineering and may break if CSFloat updates their API endpoints. Use at your own risk and consider rate limiting your requests.

## Features

- Create and manage buy orders
- Fetch your active buy orders
- Get market buy orders for specific items
- Retrieve item listings with filtering and sorting
- Monitor account balance
- Automated buy order management and undercutting

## Installation

1. Clone this repository:
```bash
git clone https://github.com/JA-Marshall/cs-float-scripts.git
cd cs-float-scripts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your CSFloat API key:
```bash
CS_FLOAT_API_KEY=your_api_key_here
```

## API Endpoints

### Account Management

#### `get_balance()` → `int`
Get your current CSFloat account balance in cents.
- **Returns**: Balance in cents (e.g., 1500 = $15.00)

### Buy Order Management

#### `get_our_buy_orders()` → `List[OurBuyOrder]`
Retrieve all your active buy orders.
- **Returns**: List of `OurBuyOrder` objects with fields:
  - `id`: Buy order ID (required for deletion)
  - `created_at`: Creation timestamp (ISO 8601 format)
  - `market_hash_name`: Item name
  - `qty`: Quantity
  - `price`: Price in cents

#### `create_buy_order(market_hash_name, max_price, quantity)` → `bool`
Create a new buy order.
- **Parameters**:
  - `market_hash_name` (str): Item name (e.g., "AK-47 | Redline (Field-Tested)")
  - `max_price` (str): Maximum price in cents (e.g., "1500" for $15.00)
  - `quantity` (str): Number of items to buy
- **Returns**: `True` if successful, `False` otherwise

#### `remove_buy_order(id)` → `bool`
Delete a buy order by ID.
- **Parameters**:
  - `id` (str): Buy order ID from `get_our_buy_orders()`
- **Returns**: `True` if successful, `False` otherwise

### Market Data

#### `get_item_buy_orders(listing_id)` → `List[MarketBuyOrder]`
Get the top buy orders for a specific item.
- **Parameters**:
  - `listing_id` (str): CSFloat listing ID (not buy order ID)
- **Returns**: List of `MarketBuyOrder` objects with fields:
  - `market_hash_name`: Item name
  - `qty`: Quantity
  - `price`: Price in cents

#### `get_listings_from_market_hash(market_hash, limit=1, sort_by="lowest_price", type="buy_now")` → `List[Listing]`
Get item listings for a specific market hash name.
- **Parameters**:
  - `market_hash` (str): Item name
  - `limit` (int): Number of listings to fetch (default: 1)
  - `sort_by` (str): Sorting method (default: "lowest_price")
  - `type` (str): Listing type (default: "buy_now")
- **Returns**: List of `Listing` objects with fields:
  - `id`: Listing ID
  - `price`: Price in cents
  - `market_hash_name`: Item name
  - `created_at`: Creation timestamp
  - `type`: Listing type
  - `is_commodity`: Whether item is a commodity
  - `type_name`: Item category

## Usage Examples

### Basic Usage

```python
from csfloat.csfloat_api import CSFloatApi
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("CS_FLOAT_API_KEY")

# Initialize the API client
csfloat = CSFloatApi(api_key)

# Check your balance
balance = csfloat.get_balance()
print(f"Current balance: ${balance / 100:.2f}")
```

### Managing Buy Orders

```python
# Create a buy order
market_hash_name = "Prisma 2 Case"
max_price = 50  # $0.50 in cents
quantity = 10

success = csfloat.create_buy_order(market_hash_name, max_price, quantity)
if success:
    print(f"Successfully created buy order for {quantity} '{market_hash_name}' at ${max_price/100:.2f} each")

# Get all your active buy orders
buy_orders = csfloat.get_our_buy_orders()
for order in buy_orders:
    print(f"Order ID: {order.id}")
    print(f"Item: {order.market_hash_name}")
    print(f"Price: ${order.price/100:.2f}")
    print(f"Quantity: {order.qty}")
    print(f"Created: {order.created_at}")
    print("---")

# Remove a buy order
if buy_orders:
    first_order_id = buy_orders[0].id
    if csfloat.remove_buy_order(first_order_id):
        print(f"Successfully removed buy order {first_order_id}")
```

### Market Analysis

```python
# Get cheapest listing for an item
listings = csfloat.get_listings_from_market_hash("AK-47 | Redline (Field-Tested)", limit=5)
for listing in listings:
    print(f"Listing {listing.id}: ${listing.price/100:.2f}")

# Get market buy orders (requires a listing ID)
if listings:
    listing_id = listings[0].id
    market_orders = csfloat.get_item_buy_orders(listing_id)
    print("Top buy orders:")
    for order in market_orders:
        print(f"Price: ${order.price/100:.2f}, Quantity: {order.qty}")
```

### Automated Buy Order Management

The included `buy_order_manager.py` demonstrates automated undercutting:

```python
#!/usr/bin/env python3
from csfloat.csfloat_api import CSFloatApi
from dotenv import load_dotenv
import os
import time

def main():
    load_dotenv()
    api_key = os.getenv("CS_FLOAT_API_KEY")
    csfloat = CSFloatApi(api_key)

    # Get your current buy orders
    our_orders = csfloat.get_our_buy_orders()

    for order in our_orders:
        # Get current market listings
        listings = csfloat.get_listings_from_market_hash(order.market_hash_name)
        if not listings:
            continue

        # Check competitor buy orders
        competitor_orders = csfloat.get_item_buy_orders(listings[0].id)
        if not competitor_orders:
            continue

        highest_bid = competitor_orders[0].price

        # If someone outbid us, update our order
        if highest_bid > order.price:
            print(f"Outbid on {order.market_hash_name}: ${highest_bid/100:.2f} > ${order.price/100:.2f}")

            # Remove old order
            if csfloat.remove_buy_order(order.id):
                # Create new order at higher price
                new_price = highest_bid + 1
                csfloat.create_buy_order(order.market_hash_name, new_price, order.qty)
                print(f"Created new order at ${new_price/100:.2f}")

        time.sleep(1)  # Rate limiting

if __name__ == "__main__":
    main()
```

## Data Models

### OurBuyOrder
Your buy orders with management capabilities:
- `id`: Unique identifier for deletion
- `created_at`: ISO 8601 timestamp
- `market_hash_name`: Item name
- `qty`: Quantity
- `price`: Price in cents

### MarketBuyOrder
Public buy orders from other users:
- `market_hash_name`: Item name
- `qty`: Quantity
- `price`: Price in cents

### Listing
Item listings on the marketplace:
- `id`: Listing identifier
- `created_at`: Creation timestamp
- `type`: Listing type ("buy_now", etc.)
- `price`: Price in cents
- `market_hash_name`: Item name
- `is_commodity`: Whether all items are identical
- `type_name`: Item category

## Rate Limiting

CSFloat's API rate limits are unknown. The example code includes 1-second delays between requests. Adjust as needed to avoid being blocked.

## Error Handling

The library includes custom exceptions in `csfloat/exceptions.py`. Wrap API calls in try-catch blocks for production use:

```python
from csfloat.exceptions import CSFloatApiException

try:
    orders = csfloat.get_our_buy_orders()
except CSFloatApiException as e:
    print(f"API Error: {e}")
```

## Contributing

Contributions are welcome! This project is licensed under the MIT License.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Disclaimer

This library is not officially affiliated with CSFloat. The API endpoints are undocumented and subject to change without notice. Use responsibly and at your own risk.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.