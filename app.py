from flask import Flask, request
import hmac
import hashlib
import json
import ccxt
import os

app = Flask(__name__)

binance_api_key = os.environ.get("BINANCE_API_KEY")
binance_api_secret = os.environ.get("BINANCE_API_SECRET")

exchange = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_api_secret,
    'enableRateLimit': True
})

@app.route('/')
def home():
    return 'Chester the bot is alive and watching...'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return 'Missing data', 400

    action = data.get('action')
    symbol = data.get('symbol', 'BTC/USDT')
    amount = float(data.get('amount', 10))  # USD amount

    try:
        price = exchange.fetch_ticker(symbol)['last']
        qty = amount / price

        if action == 'buy':
            exchange.create_market_buy_order(symbol, qty)
        elif action == 'sell':
            exchange.create_market_sell_order(symbol, qty)
        else:
            return 'Invalid action', 400

        return f"{action.upper()} order placed for {qty:.6f} {symbol}", 200

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
