def pipe(inp,xs):
    '''inp is the data , pipe inp through each function in xs all is unary function'''
    return inp if len(xs) == 0 else pipe(xs[0](inp),xs[1:])

def roll(xs,index,roll):
    '''similar to list splicing, xs is list, index is starting index, roll is how much to cut from index'''
    return xs[index:index+roll]

def get_candle(xs):
    '''get candle info from raw gemini changes'''
    return map(lambda x: roll(x,1,4) ,xs)

def get_close(xs):
    '''get close info from raw gemini changes'''
    return list(map(lambda x: x[4] ,xs))

def MA(closes,p):
    '''get MA from list of closes after calling get_close, p is period, '''
    return pipe(closes,[
        lambda inp: list(map(
            lambda index: roll(inp, index, p) ,range(len(inp) )
        )),
        lambda inp: list(map(lambda roll: pipe(roll,[sum,lambda x: x/p]),inp))
    ])

def raw_MA(xs,p):
    '''get MA with p from raw gemini changes'''
    return pipe(xs,[
            get_close,
            lambda closes: MA(closes,p)
        ])

def TR(candles,i):
    '''raw gemini changes TR depending on the i, i is usually 0'''
    curr = candles[i]
    if i+1 == len(candles):
        return 0
    prev = candles[i+1]
    HL = curr[2] - curr[3]
    AHc = abs(curr[2] - prev[4])
    ALc = abs(curr[3] - prev[4])
    return max(HL,AHc,ALc)

def ATR(candles,p):
    return pipe(candles,[
        lambda inp: list(map( lambda index : TR(inp,index) ,range(len(inp)))),
        lambda inp: MA(inp,p)
    ])