# Webhook Trader
Webhook crypto trader. Intended to be used along with TradingView and any crypto exchange.

## Current state of the project
It receives a webhook and places a Limit Order on the cryptocurrency exchange you configure. Only tested with Binance so far.

You can post it a `BUY` or `SELL` to the webhook like this. Example:
```json
{
  "exchange_id": "XXXXXXXXXX",
  "symbol": "BTC/USDT",
  "order_type": "LIMIT",
  "side": "BUY",
  "price": "11220",
  "quantity": 0.002
}
```
If you don't set `quantity`, you might want to set `amount_pc` which is a calculated percentage from your wallet for the base or quote currency. Example:
```json
{
  "exchange_id": "XXXXXXXXXX",
  "symbol": "BTC/USDT",
  "order_type": "LIMIT",
  "side": "BUY",
  "price": "11220",
  "amount_pc": 80
}
```
In this example, the `BUY` operation will take 80% of my `USDT` Spot wallet to buy `BTC` at the specified price above.

The below example uses your entire `USDT` wallet to buy `BTC` at the market price. These are the minimum required fields for it to work.
```json
{
  "exchange_id": "wht-binance",
  "symbol": "BTC/USDT",
  "order_type": "MARKET",
  "side": "BUY"
}
```

Please note the following:
- You can have any number of exchanges set up in `wht_config.py`, but the `id` field is the one you'll be calling from the webhook as `exchange_id`.
- The input values from the JSON get normalized, so if you mix uppercase with lowercase or mix a type string value with a type float, don't worry. This rule doesn't apply to the `exchange_id` field.
- If you don't set the `price` field, it will just retrieve the most recent close price for the `symbol` specified.
- If you don't set the `stop_price` field, it will take the value from the previously set `price` field.
- Valid `order_type` values are: `market`, `limit` and `stop_limit`. Any other `order_type` will just get ignored.
- Setting `quantity` and `amount_pc` at the same time will make `quantity` override `amount_pc`.
- If you don't set either `quantity` or `amount_pc`, `amount_pc` will take the default value of 100% from your Spot wallet.

## Setup instructions
1. Navigate to the cloned repository directory.
2. Create a virtual environment (e.g. `$ python -m venv venv`).
3. Activate the virtual environment (e.g. `$ source venv/bin/activate`).
4. Install package requirements (e.g. `(venv) $ pip install -r requirements.txt`).
5. Duplicate file `wht_config-sample.py` into `wht_config.py` editing it with your custom values.
6. \#TODO: Write Flask instructions here.

Developed using `Flask` and `ccxt`.
