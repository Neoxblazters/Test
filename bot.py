import websocket, json, pprint, numpy, talib

from binance.client import Client

from binance.enums import *

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

SOCKET = "wss://stream.binance.com:9443/ws/shibusdt@kline_15m"

PERIOD = 14
BUY_SIG = 40
SELL_SIG = 70
TRADE_SYM = 'SHIBUSDT'

closes = []
client = Client(config.API_KEY, config.API_SECRET)
