import websocket, json, pprint, numpy, talib, datetime, sys, time

from binance.client import Client

from binance.enums import *


in_pos = True

B_SIG = 50

L_RSI = 49

def buy_message():
    try:
        print("We are in buy_message()")
    except Exception as e:
        return False
    return True


def debug():
    if L_RSI < B_SIG:
        if in_pos:
            print("Worked..Testing Buy method")
            B_COMP = buy_message()
            if B_COMP:
                C_POS_F()
    else:
        print("Worked under else..")

def C_POS_F():
    global in_pos
    in_pos = False
    C_INPOS()

def C_INPOS():
    if in_pos:
        print("TRUE")
    else:
        print("FALSE")


debug()

