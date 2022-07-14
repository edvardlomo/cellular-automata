import numpy as np

def cell_auta_1d(n, t=110, mid=False, rnd=0):
    """Returns a 1D board with n cells, rules are given byt. If wanted a cell in middle is turned on with mid, or it can be randomised with rnd."""
    

    cond1 = lambda c, ns: c == 1 and all(ns == [1,1,1])
    cond2 = lambda c, ns: c == 1 and all(ns == [1,1,0])
    cond3 = lambda c, ns: c == 0 and all(ns == [1,0,1])
    cond4 = lambda c, ns: c == 0 and all(ns == [1,0,0])
    cond5 = lambda c, ns: c == 1 and all(ns == [0,1,1])
    cond6 = lambda c, ns: c == 1 and all(ns == [0,1,0])
    cond7 = lambda c, ns: c == 0 and all(ns == [0,0,1])
    cond8 = lambda c, ns: c == 0 and all(ns == [0,0,0])
    conds = [cond1,cond2,cond3,cond4,cond5,cond6,cond7,cond8]
    b = bin(t)[2:]
    b = "0"*(8-len(b))+b
    rules = [(cond,int(i)) for cond,i in zip(conds,b)]

    board = (np.random.rand(n) < rnd)
    if mid:
        board[n//2] = 1
    return board, rules

