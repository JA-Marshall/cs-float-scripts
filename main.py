from api import build_headers, fetch_highest_buy_order,get_our_current_buy_orders
from logger import log_to_console, log_to_discord

def main() -> None:
    """Main entry point of the script."""
    listing_id = "791974964206110791"  # Example ID, replace with dynamic input if needed

    try:
        headers = build_headers()
        get_our_current_buy_orders(headers)
        # # highest_order = fetch_highest_buy_order(int(listing_id), headers)
        # message = f"Highest buy order: {highest_order}"
        # log_to_console(message)
        # log_to_discord(message)
    except ValueError as e:
        error_message = f"Validation error: {e}"
        log_to_console(error_message, level="warning")
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        log_to_console(error_message, level="error")
        

if __name__ == '__main__':
    main()
