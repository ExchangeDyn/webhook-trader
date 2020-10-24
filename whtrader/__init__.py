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

# Local application imports
import wht_core
import wth_config

# Set variables from config file
wh_key = wth_config.wh_key

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
            recv_message = request.data.decode("utf-8")
            instruction = json.loads(recv_message)
            logger.info("POST Request received: %s", instruction)
            symbol = instruction["symbol"]
            side = instruction["side"]
            price = instruction["price"]
            quantity = instruction["quantity"]
            e.submit(wht_core.place_order,
                     symbol,
                     side,
                     price,
                     quantity)
            return 'POST OK', 200

    return app
