import websocket, json, pprint, numpy, talib, datetime, sys, time

from binance.client import Client

from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1h"

PERIOD = 5
BUY_SIG = 30
SELL_SIG = 70
TRADE_SYM = 'BTCUSDT'

closes = []

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
        print(RSI, file=open("rsi.log", "a"))

    if latest_RSI > SELL_SIG:
        print("Sell : ",file=open("all_signals.log", "a"))
        print(datetime.datetime.now(), file=open("all_signals.log", "a"))
        sig = "sig.log"
        tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
        with open(sig, 'w') as filetowrite:
            filetowrite.write('Sell at'+tm)

    if latest_RSI < BUY_SIG:
        print("Buy : ",file=open("all_signals.log", "a"))
        print(datetime.datetime.now(), file=open("all_signals.log", "a"))
        sig = "sig.log"
        tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
        with open(sig, 'w') as filetowrite:
            filetowrite.write('Buy at '+tm)
        
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
