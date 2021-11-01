import websocket, json, pprint, numpy, talib, datetime

from binance.client import Client

from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/shibusdt@kline_1m"

PERIOD = 7
BUY_SIG = 40
SELL_SIG = 70
TRADE_SYM = 'SHIBUSDT'

closes = []
in_position = True

def now():
    try:
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print("An error occured")
        return False
    return True

def on_close(ws):
    print('Monitoring stopped')

def on_open(ws):
    print('Monitoring started')

def on_message(ws, message):
    #global closes
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("Closing value {}".format(close))
        closes.append(float(close))
        print("closes")

    if len(closes) > PERIOD:
        np_closes = numpy.array(closes)
        RSI = talib.RSI(np_closes, PERIOD)
        latest_RSI = RSI[-1]
        print("The current RSI is {}".format(lastest_RSI))

    if latest_RSI > SELL_SIG:
        print("Sell signal received")
        if in_position:
            print("Advised to sell at : ")
            if now:
                in_position = False
        else:
            print("Not in position to sell")

    if latest_RSI < BUY_SIG:
        print("Buy signal received")
        if in_position:
            print("Already in position")
        else:
            print("Advised to buy at : ")
            if now:
                in_position = True

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
