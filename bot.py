import websocket, json, pprint, numpy, talib, datetime, sys, time

from binance.client import Client

from binance.enums import *

SOCK = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

PR = 2
B_SIG = 50
S_SIG = 53
T_SYM = 'BTCUSDT'

closes = []
in_pos = True

def on_open(ws):
    print('Monitoring started')

def S_MESSAGE():
    try:
        print("Sell : "+datetime.datetime.now(),file=open("signals.log", "a"))
    except Exception as e:
        print("An error occured -{}".format(e))
        return False
    return True

def B_MESSAGE():
    try:
        print("Buy : "+datetime.datetime.now(),file=open("signals.log", "a"))
    except Exception as e:
        print("An error occured -{}".format(e))
        return False
    return True

def C_POS_F():
    global in_pos
    in_pos = False

def C_POS_T():
    global in_pos
    in_pos = True

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        closes.append(float(close))
        print(closes, file=open("closes.log", "a"))

    if len(closes) > PR:
        np_closes = numpy.array(closes)
        R = talib.RSI(np_closes, PR)
        L_R = R[-1]
        f = open('closes.log', 'r+')
        f.truncate(0)
        print(R, file=open("rsi.log", "a"))
        print(L_R)

    if L_R > S_SIG:
        if in_pos:
            if is_candle_closed:
                S_COMP = S_MESSAGE()
                if S_COMP:
                    C_POS_F()
        else:
            print("Not ready to Sell")

    if L_R < B_SIG:
        if in_pos:
            print("Not ready to Buy")
        else:
            if is_candle_closed:
                B_COMP = B_MESSAGE()
                if B_COMP:
                    C_POS_T()
        
ws = websocket.WebSocketApp(SOCK, on_open=on_open, on_message=on_message)
ws.run_forever()
