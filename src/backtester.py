import requests, json
from util import util
from bot import bot,reset
#always production 
window_size = 30
def get_candles(symbol, p):
    '''symbol is like btcsgd p is like 1m'''
    base_url = "https://api.sandbox.gemini.com/v2"
    response = requests.get(base_url + f"/candles/{symbol}/{p}")
    btc_candle_data = response.json()

    return btc_candle_data

#range(last_index,-1, -1)
prev = 0
def test(t_range,all_candles,params):
    global prev
    f = open("demofile2.txt", "a")
    res = 0
    for index in t_range:
        candle_window = util.roll(all_candles,index, window_size)
        res = bot(candle_window, util,params)
        #print(res)
        
        f.write('{0:,.2f}'.format(res)+'\n')
    reset()
    f.close()
    return res

sum = 0 

def backtester(all_candles):
    global window_size, sum
    last_index = len(all_candles) - window_size
    allrange = range(last_index,-1, -1)
    print(test(allrange, all_candles,[7,8]))

    #for f in range(1,27):
    #    for s in range(f+1, 28):
    #        earn = test(allrange,all_candles,[f,s])
    #        if earn > sum:
    #            sum = earn
    #            print([f,s], sum)
            
            
