import json
import time
import pandas as pd
from constants import CLOSE_AT_ZSCORE_CROSS
from utils import format_number
from public import get_candles_recent
from cointegration import zscore
from private import market_order
from agent import BotAgent
from pprint import pprint

def exit_positions(client):
    save_output = []
    try:
        open_positions_file = open("bot_agents.json")
        open_positions_dict = json.load(open_positions_file)
    except:
        return "complete"
    if len(open_positions_dict) < 1:
        return "complete"
    exchange_pos = client.private.get_positions(status="OPEN")
    all_pos = exchange_pos.data["positions"]
    live_markets = []
    for pos in all_pos:
        live_markets.append(pos["market"])
    time.sleep(0.5)
    for pos in open_positions_dict:
        close = False

        pos_market_m1 = pos["market_1"]
        pos_size_m1 = pos["order_m1_size"]
        pos_side_m1 = pos["order_m1_side"]

        pos_market_m2 = pos["market_2"]
        pos_size_m2 = pos["order_m2_size"]
        pos_side_m2 = pos["order_m2_side"]

        order_m1 = client.private.get_order_by_id(pos["order_id_m1"])
        market_m1 = order_m1.data["order"]["market"]
        size_m1 = order_m1.data["order"]["size"]
        side_m1 = order_m1.data["order"]["side"]

        order_m2 = client.private.get_order_by_id(pos["order_id_m2"])
        market_m2 = order_m2.data["order"]["market"]
        size_m2 = order_m2.data["order"]["size"]
        side_m2 = order_m2.data["order"]["side"]
        
        m1_check = market_m1 == pos_market_m1 and pos_size_m1 == size_m1 and side_m1 == pos_side_m1
        m2_check = market_m2 == pos_market_m2 and pos_size_m2 == size_m2 and side_m2 == pos_side_m2
        live_check = pos_market_m1 in live_markets and pos_market_m2 in live_markets
        if not m1_check or not m2_check or not live_check:
            print("Error matching exchange data on positions and given open position data")
            continue
        series_1 = get_candles_recent(client, pos_market_m1)
        series_2 = get_candles_recent(client, pos_market_m2)
        markets = client.public.get_markets().data
        if CLOSE_AT_ZSCORE_CROSS:
            hedge_ratio = pos["hedge_ratio"]
            zscore_pos = pos["z_score"]
            if len(series_1) > 0 and len(series_1) == len(series_2):
                spread = series_1 - (hedge_ratio * series_2)
                zscore_curr = zscore(spread).values.tolist()[-1]
            zscore_level_check = abs(zscore_curr) >= abs(zscore_pos)
            zscore_cross_check = (zscore_curr < 0 and zscore_pos > 0) or (zscore_curr > 0 and zscore_pos < 0)
            if zscore_level_check and zscore_cross_check:
                close = True
        if close:
            side_m1 = "SELL"
            if pos_side_m1 == "SELL":
                side_m1 = "BUY"
            side_m2 = "SELL"
            if pos_side_m2 == "SELL":
                side_m2 = "BUY"
            price_m1 = float(series_1[-1])
            price_m2 = float(series_2[-1])
            accept_price_m1 = price_m1 * 1.05 if side_m1 == "BUY" else price_m1 * 0.95
            accept_price_m2 = price_m2 * 1.05 if side_m2 == "BUY" else price_m2 * 0.95
            tick_size_m1 = markets["markets"][pos_market_m1]["tickSize"]
            tick_size_m2 = markets["markets"][pos_market_m2]["tickSize"]
            accept_price_m1 = format_number(accept_price_m1, tick_size_m1)
            accept_price_m2 = format_number(accept_price_m2, tick_size_m2)
            try:
                print(f"Closing {pos_market_m1} for market 1")
                close_m1 = market_order(
                    client,
                    market=pos_market_m1,
                    side=side_m1,
                    size=pos_size_m1,
                    price=accept_price_m1,
                    reduce_only=True,
                )
                print(close_m1["order"]["id"])
                print(f"Closing {pos_market_m2} for market 2")
                close_m2 = market_order(
                    client,
                    market=pos_market_m2,
                    side=side_m2,
                    size=pos_size_m2,
                    price=accept_price_m2,
                    reduce_only=True,
                )
                print(close_m2["order"]["id"])
            except Exception as e:
                print(f"Unable to exit {pos_market_m1} with {pos_market_m2}")
                save_output.append(pos)
        else:
            save_output.append(pos)
        with open("bot_agents.json", "w") as f:
            json.dump(save_output, f)

