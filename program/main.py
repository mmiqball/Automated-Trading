from connections import connect_dydx
from constants import ABORT_ALL, FIND_COINTEGRATED, PLACE_TRADES, FIND_EXITS
from private import abort_all
from public import construct_market_prices
from cointegration import store_cointegration_results
from entry_pairs import open_positions
from exit_pairs import exit_positions
from send_updates import send_update

if __name__ == "__main__":

    send_update("Starting another run")

    try:
        print("Connected")
        client = connect_dydx()
    except Exception as e:
        print("error: ", e)
        send_update(f"Unable to connect to exchange: {e}")
        exit(1)
    
    if ABORT_ALL:
        try:
            print("All positions closed")
            abort_all(client)
        except Exception as e:
            print("error: ", e)
            send_update(f"Error encountered while aborting all positions: {e}")
            exit(1)
    if FIND_COINTEGRATED:
        try:
            print("Retrieving Market Data")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("error: ", e)
            send_update(f"Error encountered while building market prices: {e}")
            exit(1)
    



        try:
            print("Analyzing cointegration")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error in analyzing cointegration: ", e)
            send_update(f"Error encountered while analyzing cointegration: {e}")
            exit(1)

    while True:

        if FIND_EXITS:
            try:
                print("Closing redundant trades")
                exit_positions(client)
            except Exception as e:
                print("Error exiting trades: ", e)
                send_update(f"Error encountered while attempting to exit trades: {e}")
                exit(1)

        if PLACE_TRADES:
            try:
                print("Opening positions")
                open_positions(client)
            except Exception as e:
                print("Error opening trades: ", e)
                send_update(f"Error encountered while opening positions: {e}")
                exit(1)