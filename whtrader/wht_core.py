# -*- coding: utf-8 -*-

# Standard library imports
import logging

logger = logging.getLogger(__name__)


def wh_index():
    redirect = '<head><meta http-equiv="refresh" content="0; URL=\'https://www.google.com\'" /></head>'
    return redirect


def fetch_asset_balance(exchange, asset):
    balances = exchange.fetch_balance()
    return balances["free"][asset]


def determine_quantity(side, amount_pc, balance, price):
    amount_pc = float(amount_pc)
    balance = float(balance)
    price = float(price)
    quantity = 0
    if side == "BUY":
        quantity = amount_pc / 100 * balance / price
    if side == "SELL":
        quantity = amount_pc / 100 * balance
    return quantity


def place_order(exchange, symbol, side, price, quantity):
    if side == "BUY":
        print("LIMIT ORDER", symbol, side, price, quantity)
        order = exchange.create_limit_buy_order(symbol, quantity, price)
    elif side == "SELL":
        print("LIMIT ORDER", symbol, side, price, quantity)
        order = exchange.create_limit_sell_order(symbol, quantity, price)
    return order
