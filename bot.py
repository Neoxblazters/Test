import websocket, json, pprint, numpy, talib, datetime, sys

from binance.client import Client

from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/shibusdt@kline_1m"

PERIOD = 2
BUY_SIG = 40
SELL_SIG = 70
TRADE_SYM = 'SHIBUSDT'

closes = []

old_stdout = sys.stdout
log_sell = open("sell_signals.log")
log_buy = open("buy_signals.log")
log_closes = open("closes.log")
log_rsi = open("rsi.log")

def on_close(ws):
    print('Monitoring stopped')

def on_open(ws):
    print('Monitoring started')

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        closes.append(float(close))
        print(closes, file=open("closes.log", "a"))

    if len(closes) > PERIOD:
        np_closes = numpy.array(closes)
        RSI = talib.RSI(np_closes, PERIOD)
        latest_RSI = RSI[-1]
        f = open('closes.log', 'r+')
        f.truncate(0)
        print(closes, file=open("closes.log", "a"))
        print(latest_RSI, file=open("rsi.log", "a"))

    if latest_RSI > SELL_SIG:
        now = datetime.datetime.now()
        print("Sell signal received", file=open("sell_signals.log"))
        print(now.strftime("%Y-%m-%d %H:%M:%S", file=open("sell_signals.log")))

    if latest_RSI < BUY_SIG:
        now = datetime.datetime.now()
        print("Buy signal received", file=open("buy_signals.log"))
        print(now.strftime("%Y-%m-%d %H:%M:%S", file=open("buy_signals.log")))
        
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
