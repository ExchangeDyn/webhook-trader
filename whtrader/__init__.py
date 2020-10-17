# -*- coding: utf-8 -*-

# Standard library imports
import logging.config
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
import json
import locale
import os
from concurrent.futures import ThreadPoolExecutor

# Third party imports
from flask import Flask, request, make_response  # , abort

# Local application imports


# Set variables from config file


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
        return idb_core.bot_index(), 301


    # ip-addr route for troubleshooting purposes
    @app.route('/ip-addr')
    def ip_addr():
        ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return ip_address, 200


    # main webhook
    @app.route('/' + bot_key + '/webhook', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            recv_message = request.data.decode("utf-8")
            msg = json.loads(recv_message)
            logger.debug('JSON Message: %s', recv_message)
            try:
                command = msg['message']['text'].replace('/', '')
                command = command.lower().strip()
                user_id = msg['message']['from']['id']
                chat_id = msg['message']['chat']['id']
                if command == 'start' or command == 'ayuda':
                    logger.info('POST Request received: %s for %s', command.upper(), user_id)
                    e.submit(idb_core.t_start_message, user_id, 'Markdown', '1')
                if command == 'usd' or command == 'usd' + bot_username:
                    logger.info('POST Request received: %s for %s', command.upper(), chat_id)
                    e.submit(idb_core.t_get_latest_quote, chat_id, 'USD', 'Markdown', '1')
                if command == 'dolar' or command == 'dolar' + bot_username:
                    logger.info('POST Request received: %s for %s', command.upper(), chat_id)
                    e.submit(idb_core.t_render_latest_quote, chat_id, 'USD', 'Markdown', '1', '0')
                if command == 'eur' or command == 'eur' + bot_username:
                    logger.info('POST Request received: %s for %s', command.upper(), chat_id)
                    e.submit(idb_core.t_get_latest_quote, chat_id, 'EUR', 'Markdown', '1')
                if command == 'euro' or command == 'euro' + bot_username:
                    logger.info('POST Request received: %s for %s', command.upper(), chat_id)
                    e.submit(idb_core.t_render_latest_quote, chat_id, 'EUR', 'Markdown', '1', '0')
            except KeyError:
                logger.info('Received a request, but not a message.')
                pass
            logger.info('End of current POST request.')
            try:
                if command.startswith('dolar') or command.startswith('euro'):
                    action = 'upload_photo'
                else:
                    action = 'typing'
                resp = make_response(
                    {"method": "sendChatAction",
                     "chat_id": chat_id,
                     "action": action}
                )
                resp.headers['Content-Type'] = 'application/json'
                return resp
            except UnboundLocalError:
                return 'POST OK', 200

    return app
