# Webhook Trader
Webhook crypto trader. Intended to be used along with TradingView and a crypto exchange.

## Current state of the project
It receives a webhook and places a Take Profit Order or a Stop Limit Order on Binance.

You can post it a `BUY` or `SELL` to the webhook like this. Example:
```json
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "time_in_force": "GTC",
  "trigger_price": "11200",
  "price": "11220",
  "quantity": 0.002
}
```

## Setup instructions
1. Navigate to the cloned repository directory.
2. Create a virtual environment (e.g. `$ python -m venv venv`).
3. Activate the virtual environment (e.g. `$ source venv/bin/activate`).
4. Install package requirements (e.g. `(venv) $ pip install -r requirements.txt`).
5. Duplicate file `wth_config-sample.py` into `wth_config.py`editing it with your custom values.
6. \#TODO: Write Flask instructions here.

Developed using `Flask` and `python-binance`.
