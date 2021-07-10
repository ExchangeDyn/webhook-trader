# -*- coding: utf-8 -*-

# Standard library imports
import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Third party imports
from flask import Flask, request, make_response  # , abort
import ccxt

# Local application imports
import wht_core
import wht_config

# Create exchange instances from config file and grab other settings
wh_key = wht_config.wh_key
exchanges = wht_config.exchanges
instances = {}

for i in exchanges:
    exchange_id = i["id"]
    exchange_type = i["type"]
    exchange_params = i["params"]
    exchange_class = getattr(ccxt, exchange_type)
    instances[exchange_id] = exchange_class(exchange_params)

# Set threading pool
e = ThreadPoolExecutor()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # main route
    @app.route("/")
    def index():
        return wht_core.wh_index(), 301

    # ip-addr route for troubleshooting purposes
    @app.route("/ip-addr")
    def ip_addr():
        ip_address = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
        return ip_address, 200

    # main webhook
    @app.route("/" + wh_key + "/webhook", methods=["POST"])
    def webhook():
        if request.method == "POST":
            msg_posted = request.data.decode("utf-8")
            instruction = json.loads(msg_posted)
            logger.info("POST Request received: %s", instruction)
            instance_ref = instruction["exchange_id"]
            exchange = instances[instance_ref]
            symbol = instruction["symbol"].upper()
            order_type = instruction["order_type"].lower()
            side = instruction["side"].lower()
            try:
                price = instruction["price"]
            except KeyError:
                price = exchange.fetchTicker(symbol)["close"]
            try:
                stop_price = instruction["stop_price"]
            except KeyError:
                stop_price = price
            try:
                amount_pc = instruction["amount_pc"]
            except KeyError:
                amount_pc = 100
            quantity = 0
            try:
                quantity = instruction["quantity"]
            except KeyError:
                if side == "buy":
                    balance_quote = wht_core.fetch_asset_balance(
                        exchange, symbol.split("/")[1].upper()
                    )
                    quantity = wht_core.determine_quantity(
                        side, amount_pc, balance_quote, price
                    )
                elif side == "sell":
                    balance_base = wht_core.fetch_asset_balance(
                        exchange, symbol.split("/")[0].upper()
                    )
                    quantity = wht_core.determine_quantity(
                        side, amount_pc, balance_base, price
                    )

            # Submit order for execution
            e.submit(
                wht_core.place_order,
                exchange=exchange,
                symbol=symbol,
                order_type=order_type,
                side=side,
                quantity=quantity,
                price=price,
                stop_price=stop_price,
            )
            return "POST OK", 200

    return app
