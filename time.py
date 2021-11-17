#import datetime, os
import websocket, json, pprint, numpy, talib, datetime, sys, re, time




print("Sell signal received", file=open("sell_signals.log", "a"))
print(datetime.datetime.now(), file=open("sell_signals.log", "a"))

sell_sig = "sig.log"
tm = time.strftime('%a, %d %b %Y %H:%M:%S %Z(%z)')
with open(sell_sig, 'w') as filetowrite:
    filetowrite.write('received'+tm)
