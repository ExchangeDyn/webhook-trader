# -*- coding: utf-8 -*-

# Standard library imports
import logging
logger = logging.getLogger(__name__)

# Third party imports
from binance.client import Client
from binance.enums import *

# Local application imports
import wth_config

# Set variables from config file
binance_api_key = wth_config.binance_api_key
binance_secret_key = wth_config.binance_secret_key
binance_client = Client(api_key=binance_api_key,
                        api_secret=binance_secret_key)


def wh_index():
    redirect = '<head><meta http-equiv="refresh" content="0; URL=\'https://www.google.com\'" /></head>'
    return redirect


def stop_loss_or_take_profit(side, trigger_price, price):
    if side == SIDE_BUY:
        if trigger_price >= price:
            return ORDER_TYPE_STOP_LOSS_LIMIT
        else:
            return ORDER_TYPE_TAKE_PROFIT_LIMIT
    if side == SIDE_SELL:
        if trigger_price <= price:
            return ORDER_TYPE_STOP_LOSS_LIMIT
        else:
            return ORDER_TYPE_TAKE_PROFIT_LIMIT
    # if side is not properly specified, fail with None
    return None


def create_order(symbol, side, time_in_force, trigger_price, price, quantity):
    # Align to library's enums
    if side == 'BUY':
        side = SIDE_BUY
    elif side == 'SELL':
        side = SIDE_SELL
    if time_in_force == 'GTC':
        time_in_force = TIME_IN_FORCE_GTC
    elif time_in_force == 'FOK':
        time_in_force = TIME_IN_FORCE_FOK
    elif time_in_force == 'IOC':
        time_in_force = TIME_IN_FORCE_IOC

    order_type = stop_loss_or_take_profit(side, trigger_price, price)
    order = binance_client.create_order(symbol=symbol,
                                side=side,
                                type=order_type,
                                timeInForce=time_in_force,
                                stopPrice=trigger_price,
                                price=price,
                                quantity=quantity)
    return order


