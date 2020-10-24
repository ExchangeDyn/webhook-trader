# Webhook Trader
Webhook crypto trader. Intended to be used along with TradingView and any crypto exchange.

## Current state of the project
It receives a webhook and places a Limit Order on Binance.

You can post it a `BUY` or `SELL` to the webhook like this. Example:
```json
{
  "symbol": "BTC/USDT",
  "side": "BUY",
  "price": "11220",
  "quantity": 0.002
}
```
If you don't set `quantity`, you might want to set `amount_pc` which is a calculated percentage from your wallet for the base or quote currency. Example:
```json
{
  "symbol": "BTC/USDT",
  "side": "BUY",
  "price": "11220",
  "amount_pc": 80
}
```
In this example, the `BUY` operation will take 80% of my `USDT` Spot wallet to buy `BTC` at the specified price above.

Please note the following:
- Setting `quantity` and `amount_pc` at the same time will make `quantity` override `amount_pc`.
- If you don't set both `quantity` and `amount_pc`, `amount_pc` will take a the default value of 100% from your Spot wallet.

## Setup instructions
1. Navigate to the cloned repository directory.
2. Create a virtual environment (e.g. `$ python -m venv venv`).
3. Activate the virtual environment (e.g. `$ source venv/bin/activate`).
4. Install package requirements (e.g. `(venv) $ pip install -r requirements.txt`).
5. Duplicate file `wth_config-sample.py` into `wth_config.py`editing it with your custom values.
6. \#TODO: Write Flask instructions here.

Developed using `Flask` and `ccxt`.
