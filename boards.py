from logic import *
from collections import defaultdict
import numpy as np


def get_board(w,h,rnd=0):
    return (np.random.rand(w*h) < rnd).reshape((w,h)).astype('int')

def moore_neighbors():
    """Returns functions allowing for moore neighbors, both cardinal and diagonal directions"""
    # Slice function 
    slice_func = lambda i, j: np.s_[max(i - 1,0):i + 2, max(j-1, 0):j + 2]

    # Edge cases
    def edges_f(board, ns, pos_i, pos_j):
        i,j = 1,1
        if pos_i == 0:
            i -= 1
        if pos_j == 0:
            j -= 1
        c = ns[j,i]
        ns = defaultdict(lambda:0,zip(*np.unique(ns, return_counts=True)))
        ns["c"] = c
        return ns

    edges = edges_f

    # Cell function
    c_func = lambda ns: ns["c"]
    return slice_func, edges, c_func

def von_neumann_neighbors():
    """Returns functions allowing for von neumann neighbors, only based on cardinal directions"""
    # Edges
    def edges_f(board, ns, pos_i, pos_j):
        ns = defaultdict(lambda:0)
        ns["c"] = board[pos_i, pos_j]
        ns["l"] = board[pos_i, pos_j - 1]
        if pos_j == board.shape[1] - 1:
            ns["r"] = board[pos_i, 0]
        else:
            ns["r"] = board[pos_i, pos_j + 1]
        ns["t"] = board[pos_i - 1, pos_j]
        if pos_i == board.shape[1] - 1:
            ns["b"] = board[0, pos_j]
        else:
            ns["b"] = board[pos_i + 1,  pos_j]
        return ns

    edges = edges_f

    # Cell function
    c_func = lambda ns: ns["c"]
    return (lambda i, j: None), edges, c_func

def cell_auto_1d(n, t=110, mid=False, rnd=0, rules=None, slice_func=None, edges=None, c_func=None):
    """Returns a 1D board with n cells, rules are given by t. If wanted a cell in middle is turned on with mid, or it can be randomised with rnd."""

    # Rules
    if rules == None:
        cond1 = lambda c, ns: c == 1 and np.array_equal(ns, [1,1,1])
        cond2 = lambda c, ns: c == 1 and np.array_equal(ns, [1,1,0])
        cond3 = lambda c, ns: c == 0 and np.array_equal(ns, [1,0,1])
        cond4 = lambda c, ns: c == 0 and np.array_equal(ns, [1,0,0])
        cond5 = lambda c, ns: c == 1 and np.array_equal(ns, [0,1,1])
        cond6 = lambda c, ns: c == 1 and np.array_equal(ns, [0,1,0])
        cond7 = lambda c, ns: c == 0 and np.array_equal(ns, [0,0,1])
        cond8 = lambda c, ns: c == 0 and np.array_equal(ns, [0,0,0])
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

    args = (rules, slice_func, edges, c_func)
    progress = lambda b: get_next_board(b, *args)

    board = (np.random.rand(n) < rnd)
    if mid:
        board[n//2] = 1
    return board, progress


def BS_notation(w, h, B=[3], S=[2,3], rnd=0, rules=None):
    """Returns a 2D wxh board. It can be randomised with rnd. Rules follow B/S notation, B for born, S for survival, the numbers in the lists refer to living neighbors."""

    # Rules
    if rules == None:
        rules = [((lambda c, ns: c == 0 and ns[1] in B),1),
                ((lambda c, ns: c == 1 and ns[1]-1 not in S),0)]

    # Moore neighbors
    slice_func, edges, c_func = moore_neighbors()

    args = (rules, slice_func, edges, c_func)
    progress = lambda b: get_next_board(b, *args)

    return get_board(w,h,rnd), progress

def wireworld(w, h, rnd=0, rules=None, slice_func=None, edges=None, c_func=None):
    """Returns a 2D wxh board. It can be randomised with rnd. Rules are based on wireworld by Brian Silverman."""

    # Rules
    wire = 1
    electron_head = 4
    electron_tail = 2
    if rules == None:
        cond1 = (lambda c, ns: c == electron_head),electron_tail
        cond2 = (lambda c, ns: c == electron_tail),wire
        cond3 = (lambda c, ns: c == wire and ns[electron_head] in [1,2]),electron_head
        cond4 = (lambda c, ns: c == wire),wire
        rules = [cond1, cond2, cond3, cond4]

    # Moore neighbors
    slice_func, edges, c_func = moore_neighbors()

    args = (rules, slice_func, edges, c_func)
    progress = lambda b: get_next_board(b, *args)

    return get_board(w,h,rnd), progress

def brians_brain(w, h, rnd=0, rules=None, slice_func=None, edges=None, c_func=None):
    """Returns a 2D wxh board. It can be randomised with rnd. Rules are based on Brian's brain by Brian Silverman."""

    # Rules
    if rules == None:
        cond1 = (lambda c, ns: c == 0 and ns[1] == 2), 1
        cond2 = (lambda c, ns: c == 1), 2
        cond3 = (lambda c, ns: c == 2), 0
        rules = [cond1, cond2, cond3]

    # Moore neighbors
    slice_func, edges, c_func = moore_neighbors()

    args = (rules, slice_func, edges, c_func)
    progress = lambda b: get_next_board(b, *args)

    return get_board(w,h,rnd), progress

def traffic_model(w, h, rnd=(0,0), rules=None, slice_func=None, edges=None, c_func=None, tight=False):
    """Returns a 2D wxh board. It can be randomised with rnd. Rules are based on Biham-Middleton-Levine traffic model."""
    # Rules
    road = 0
    car_rm = 2 # right moving car
    car_ru = 3 # right parked car
    car_bm = 4 # down moving car
    car_bu = 5 # down parked car
    if rules == None:
        c0 = (lambda c, ns: c == road and ns["l"] == car_rm), car_ru
        c1 = (lambda c, ns: c == car_rm and ns["r"] == road), road
        c2 = (lambda c, ns: c == road and ns["t"] == car_bm), car_bu
        c3 = (lambda c, ns: c == car_bm and ns["b"] == road), road
        c4 = (lambda c, ns: c == car_rm), car_ru
        c5 = (lambda c, ns: c == car_ru), car_rm
        c6 = (lambda c, ns: c == car_bm), car_bu
        c7 = (lambda c, ns: c == car_bu), car_bm
        rules = [c0, c1, c2, c3, c4, c5, c6, c7]

    # von Neumann neighbors
    slice_func, edges, c_func = von_neumann_neighbors()

    args = (rules, slice_func, edges, c_func)
    progress = lambda b: get_next_board(b, *args)

    board = np.array([road if e < rnd[0] else car_rm if e < rnd[1] else car_bu \
            for e in np.random.rand(w*h)]).reshape((w,h)).astype('int')
    return board, progress



