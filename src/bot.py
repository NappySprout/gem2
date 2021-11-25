from time import sleep
def up(fast,slow):
    return fast > slow

time = 0
open_price = 0
earning = 0
SL = 0
trail = 0


def bot(candle,util,params):
    #sleep(1)
    global time, open_price, earning, SL, trail 
    longterm_MA = util.raw_MA(candle,200)
    if util.get_close(candle)[0] < longterm_MA[0]:
        return earning

    #slow_p = 25
    #fast_p = 20

    slow_MA = util.raw_MA(candle,params[1])
    fast_MA = util.raw_MA(candle,params[0])
    current_ATR = util.ATR(candle,14)[0]

    if up(fast_MA[0],slow_MA[0]) and not up(fast_MA[1],slow_MA[1]):
        open_price = util.get_close(candle)[0]
        trail = current_ATR*1.5
        SL = open_price - trail
        #print("beginning of upward trend", open_price)



    elif up(fast_MA[0],slow_MA[0]):
        if open_price == 0:
            #print("haven't open")
            return earning
            
        if util.get_close(candle)[0] - trail > SL: #TRAILING LOGIC good
            SL = util.get_close(candle)[0] - trail
            time += 1
            #rint("increase SL :) ", time)
            
        elif util.get_close(candle)[0] < SL: #GET OUT OF TRADE bad
            PROFIT = util.get_close(candle)[0] - open_price
            earning += PROFIT
            #print("time to bounce", "close: ",util.get_close(candle)[0] ,"profit: ", util.get_close(candle)[0] - open_price) 
            time, open_price, SL, trail = 0,0,0,0


        elif SL == 0:
            pass
            #print("waiting")
        else: #not increasing but not out either
            time += 1
            #print("currently in up trend", time)
        



        

    elif not up(fast_MA[0],slow_MA[0]) and up(fast_MA[1],slow_MA[1]):
        time = 0
        if open_price == 0:
            #print("haven't open")
            pass
        else:
            #print("close: ",util.get_close(candle)[0] ,"profit: ", util.get_close(candle)[0] - open_price)
            earning += util.get_close(candle)[0] - open_price
    return earning

        
    #else:
    #    print("chillin",fast_MA[0], slow_MA[0])
def reset():
    global time, open_price, earning, SL, trail 
    time, open_price, earning, SL, trail = 0,0,0,0,0

