import ssl
import websocket
import _thread as thread
import json

from util import util
from bot import bot

production = False
init_p = 30
base_url ="wss://api.gemini.com/v2/marketdata" if production else "wss://api.sandbox.gemini.com/v2/marketdata"

memlist = []

def on_message(ws, message):
    data = json.loads(message)
    #type , timestamp
    #type, symbol, changes
    if "changes" in data:
        global memlist
        memlist = data["changes"][:init_p] + memlist[:init_p-1] #update memlist
        bot(memlist,util)


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(logon_msg)
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    logon_msg = '{"type": "subscribe","subscriptions":[{"name":"candles_1m","symbols":["BTCSGD"]}]}'
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(base_url,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close,
                                on_open = on_open)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})