# -*- coding: utf-8 -*-

# Standard library imports
import logging
logger = logging.getLogger(__name__)

# Third party imports
import ccxt

# Local application imports
import wth_config

# Set variables from config file
api_key = wth_config.api_key
secret_key = wth_config.secret_key
exchange = wth_config.exchange
if exchange == 'binance':
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True
    })


def wh_index():
    redirect = '<head><meta http-equiv="refresh" content="0; URL=\'https://www.google.com\'" /></head>'
    return redirect


def fetch_asset_balance(exchange, asset):
    balances = exchange.fetch_balance()
    return balances['free'][asset]


def place_order(symbol, side, price, quantity):
    if side == 'BUY':
        order = exchange.create_limit_buy_order(symbol, quantity, price)
    else:
        order = exchange.create_limit_sell_order(symbol, quantity, price)
    return order
