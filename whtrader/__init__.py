# -*- coding: utf-8 -*-

# Standard library imports
import logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Third party imports
from flask import Flask, request, make_response  # , abort
import ccxt

# Local application imports
import wht_core
import wth_config

# Set variables from config file
wh_key = wth_config.wh_key
api_key = wth_config.api_key
secret_key = wth_config.secret_key
exchange = wth_config.exchange
if exchange == 'binance':
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True
    })

# Set threading pool
e = ThreadPoolExecutor()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'idb.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # main route
    @app.route('/')
    def index():
        return wht_core.wh_index(), 301

    # ip-addr route for troubleshooting purposes
    @app.route('/ip-addr')
    def ip_addr():
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return ip_address, 200

    # main webhook
    @app.route('/' + wh_key + '/webhook', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            msg_posted = request.data.decode("utf-8")
            instruction = json.loads(msg_posted)
            logger.info('POST Request received: %s', instruction)
            symbol = instruction['symbol']
            side = instruction['side']
            price = instruction['price']
            try:
                amount_pc = instruction['amount_pc']
            except KeyError:
                amount_pc = 100
            quantity = 0
            try:
                quantity = instruction['quantity']
            except KeyError:
                if side == 'BUY':
                    balance_quote = wht_core.fetch_asset_balance(exchange, symbol.split('/')[1])
                    quantity = wht_core.determine_quantity(side, amount_pc, balance_quote, price)
                elif side == 'SELL':
                    balance_base = wht_core.fetch_asset_balance(exchange, symbol.split('/')[0])
                    quantity = wht_core.determine_quantity(side, amount_pc, balance_base, price)
            e.submit(wht_core.place_order,
                     exchange=exchange,
                     symbol=symbol,
                     side=side,
                     price=price,
                     quantity=quantity)
            return 'POST OK', 200

    return app
