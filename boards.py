from logic import *
from collections import defaultdict
import numpy as np

def cell_auta_1d(n, t=110, mid=False, rnd=0, rules=None, slice_func=None, edges=None, c_func=None, state_dict=defaultdict(lambda:None)):
    """Returns a 1D board with n cells, rules are given by t. If wanted a cell in middle is turned on with mid, or it can be randomised with rnd."""

    # Rules
    if rules == None:
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
    
    # Slice function 
    if slice_func == None:
        slice_func = lambda i: slice(max(i-1,0), i+2)

    # Edge cases
    if edges == None:
        edges = lambda board, ns, pos_i: np.r_[np.zeros(1),ns] if pos_i == 0 \
                else np.r_[ns, np.zeros(1)] if pos_i == board.shape[0]-1 \
                else ns

    # Cell function
    if c_func == None:
        c_func = lambda ns: ns[1]

    args = (rules, slice_func, edges, c_func, state_dict)
    progress = lambda b: get_next_board(b, *args)

    board = (np.random.rand(n) < rnd)
    if mid:
        board[n//2] = 1
    return board, progress

def conways_game_of_life(w, h, rnd=0, rules=None, slice_func=None, edges=None, c_func=None, state_dict=defaultdict(lambda:None)):
    """Returns a 2D wxh board. It can be randomised with rnd. Rules are based on conway's game of life"""

    # Rules
    if rules == None:
        cond1 = lambda c, ns: c == 1 and ns.sum() - 1 < 2
        cond2 = lambda c, ns: c == 1 and ns.sum() - 1 > 3
        cond3 = lambda c, ns: c == 0 and ns.sum() == 3
        rules = [(cond1, 0), (cond2, 0), (cond3, 1)]
    
    # Slice function 
    if slice_func == None:
        slice_func = lambda i, j: np.s_[max(i - 1,0):i + 2, max(j-1, 0):j + 2]

    # Edge cases
    def edges_f(board, ns, pos_i, pos_j):
        if pos_i == 0:
            ns = np.c_[np.zeros(ns.shape[0]), ns]
        elif pos_i == board.shape[0] - 1:
            ns = np.c_[ns, np.zeros((ns.shape[0], 1))]
        if pos_j == 0:
            ns = np.r_[np.zeros((1,ns.shape[1])), ns]
        elif pos_j == board.shape[0] - 1:
            ns = np.r_[ns, np.zeros((1,ns.shape[1]))]
        return ns
    if edges == None:
        edges = edges_f

    # Cell function
    if c_func == None:
        c_func = lambda ns: ns[1,1]

    args = (rules, slice_func, edges, c_func, state_dict)
    progress = lambda b: get_next_board(b, *args)

    board = (np.random.rand(w*h) < rnd).reshape((w,h))
    return board, progress


