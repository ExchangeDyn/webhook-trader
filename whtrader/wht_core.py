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
    if side == "buy":
        quantity = amount_pc / 100 * balance / price
    if side == "sell":
        quantity = amount_pc / 100 * balance
    return quantity


def place_order(
    exchange, symbol, order_type, side, quantity, price=None, stop_price=None
):
    exchange = exchange
    # exchange_id = exchange.id
    symbol = symbol.upper()
    order_type = order_type.lower()
    side = side.lower()
    amount = quantity
    try:
        price = float(price)
    except TypeError:
        price = None
    try:
        stop_price = float(stop_price)
    except TypeError:
        stop_price = None
    ref_price = None
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

            ref_price = exchange.fetchTicker(symbol)["close"]

            if side == "buy" and ref_price >= stop_price:
                order = exchange.create_order(
                    symbol, "TAKE_PROFIT_LIMIT", side, amount, price, params
                )
            elif side == "buy" and ref_price < stop_price:
                order = exchange.create_order(
                    symbol, "STOP_LOSS_LIMIT", side, amount, price, params
                )
            elif side == "sell" and ref_price >= stop_price:
                order = exchange.create_order(
                    symbol, "STOP_LOSS_LIMIT", side, amount, price, params
                )
            elif side == "sell" and ref_price < stop_price:
                order = exchange.create_order(
                    symbol, "TAKE_PROFIT_LIMIT", side, amount, price, params
                )

        elif order_type == "market":
            order = exchange.create_order(symbol, order_type, side, amount)
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
            ref_price,
        )

    return order
