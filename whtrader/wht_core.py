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
    if side == "BUY".lower():
        quantity = amount_pc / 100 * balance / price
    if side == "SELL".lower():
        quantity = amount_pc / 100 * balance
    return quantity


def place_order(exchange, symbol, order_type, side, quantity, price, stop_price):
    exchange = exchange
    exchange_id = exchange.id
    symbol = symbol.upper()
    order_type = order_type.lower()
    side = side.lower()
    amount = quantity
    price = float(price)
    stop_price = float(stop_price)
    order = None

    possible_orders = [
        "market",
        "limit",
        "stop_limit",
    ]

    if order_type in possible_orders:
        if order_type == "stop_limit":
            params = {
                "stopPrice": stop_price,
                "type": "stopLimit",
            }

            # TODO: Define the logic for BUY and for SELL sides with STOP_LOSS_LIMIT and TAKE_PROFIT_LIMIT (Binance)
            order = exchange.create_order(
                symbol, "STOP_LOSS_LIMIT", side, amount, price, params
            )
        else:
            order = exchange.create_order(symbol, order_type, side, amount, price)

        print(
            f"{order_type.upper()} ORDER",
            symbol,
            order_type,
            side,
            amount,
            price,
            stop_price,
        )

    return order
