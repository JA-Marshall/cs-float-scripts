from api import build_headers, fetch_highest_buy_order, get_our_current_buy_orders, get_listing_id_from_market_hash
from logger import log_to_console

def main() -> None:
    """Main entry point of the script."""
    listing_id = "791974964206110791"  # Example ID, replace with dynamic input if needed

    try:
        log_to_console("Starting the application...", level="info")
        headers = build_headers()
        buy_orders = get_our_current_buy_orders(headers)
        log_to_console(f"Buy orders retrieved: {buy_orders}", level="info")

        test_market_hash = buy_orders[0]['market_hash_name']
        get_listing_id_from_market_hash(headers,test_market_hash)
        # highest_order = fetch_highest_buy_order(int(listing_id), headers)
        # log_to_console(f"Highest buy order: {highest_order}", level="info")

    except ValueError as e:
        error_message = f"Validation error: {e}"
        log_to_console(error_message, level="warning")
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        log_to_console(error_message, level="error")

if __name__ == '__main__':
    main()
