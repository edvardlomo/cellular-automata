from logic import *
from boards import *
from collections import defaultdict
import numpy as np
import time
import pygame


black = (0,0,0)
white = (255,255,255)

def show(screen, W,H, board):
    if len(board.shape) == 1:
        board = np.array([board])
    n = board.shape[1]
    s = W//n
    i,j = 10,10
    for j,r in enumerate(board):
        for i,c in enumerate(r):
            x,y = i*s, (j*s) % H
            if c == 1:
                pygame.draw.rect(screen, white, pygame.Rect(x,y,s,s))
            else:
                pygame.draw.rect(screen, black, pygame.Rect(x,y,s,s))

def __main__():
    """
    s = 500
    board = np.zeros((s,)).astype('int')
    board[s//2] = 1

    state_dict = defaultdict(lambda: None)
    cond1 = lambda c, ns: c == 1 and all(ns == [1,1,1])
    cond2 = lambda c, ns: c == 1 and all(ns == [1,1,0])
    cond3 = lambda c, ns: c == 0 and all(ns == [1,0,1])
    cond4 = lambda c, ns: c == 0 and all(ns == [1,0,0])
    cond5 = lambda c, ns: c == 1 and all(ns == [0,1,1])
    cond6 = lambda c, ns: c == 1 and all(ns == [0,1,0])
    cond7 = lambda c, ns: c == 0 and all(ns == [0,0,1])
    cond8 = lambda c, ns: c == 0 and all(ns == [0,0,0])

    rules = [(cond1, 0),
            (cond2, 1),
            (cond3, 0),
            (cond4, 1),
            (cond5, 1),
            (cond6, 0),
            (cond7, 1),
            (cond8, 0)]
    """
    board, rules = cell_auta_1d(100, 182, mid=True)
    state_dict = defaultdict(lambda:None)

    slice_func = lambda i: slice(max(i-1,0), i+2)
    edges = lambda board, ns, pos_i: np.r_[np.zeros(1),ns] if pos_i == 0 \
            else np.r_[ns, np.zeros(1)] if pos_i == board.shape[0]-1 \
            else ns
    c_func = lambda ns: ns[1]

    args = (rules, slice_func, edges, c_func, state_dict)
    history = np.array([board])

    # graphics
    W,H = 1000, 1000
    pygame.init()
    screen = pygame.display.set_mode((W,H))

    history_bool = 1
    loop_bool = True
    play_bool = False
    tp = 0
    spd = 2
    acc = 1000
    while loop_bool:
        tn = round(time.time()*acc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_bool = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    board = get_next_board(board, *args)
                    if history_bool:
                        history = np.r_[history, [board]]
                elif event.key == pygame.K_p:
                    play_bool = not play_bool
                elif event.key == pygame.K_ESCAPE:
                    loop_bool = False

        tf = tn - tp
        if play_bool and tf % spd == 1:
            tp = tn
            board = get_next_board(board, *args)
            if history_bool:
                history = np.r_[history, [board]]

        screen.fill(black)
        if history_bool:
            show(screen, W,H, history)
        else:
            show(screen, W,H, board)
        pygame.display.update()

if __name__ == "__main__":
    __main__()
