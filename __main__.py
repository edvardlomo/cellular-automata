from logic import *
import numpy as np
import pygame
from collections import defaultdict


def board_loop():
    pygame.init()
    screen = pygame.display.set_mode((1000,1000))
    black = (0,0,0)
    white = (255,255,255)

    loop_bool = True
    while loop_bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_bool = False
        screen.fill(black)
        pygame.draw.rect(screen, black, pygame.Rect(1,1,2,2))
        pygame.display.update()

#board_loop()
def __main__():
    s = 20
    board = np.zeros((s,)).astype('int')
    board[s//2] = 1
    history = []

    cond1 = lambda c, ns: c == 1 and all(ns == [1,1,1]) #0
    cond2 = lambda c, ns: c == 1 and all(ns == [1,1,0]) #0
    cond3 = lambda c, ns: c == 1 and all(ns == [0,1,1]) #1
    cond4 = lambda c, ns: c == 1 and all(ns == [0,1,0]) #1
    cond5 = lambda c, ns: c == 0 and all(ns == [1,0,1]) #0
    cond6 = lambda c, ns: c == 0 and all(ns == [1,0,0]) #1
    cond7 = lambda c, ns: c == 0 and all(ns == [0,0,1]) #1
    cond8 = lambda c, ns: c == 0 and all(ns == [0,0,0]) #0

    rules = [(cond1, 0),
            (cond2, 0),
            (cond3, 1),
            (cond4, 1),
            (cond5, 0),
            (cond6, 1),
            (cond7, 1),
            (cond8, 0)]

    state_dict = defaultdict(lambda: rules)

    print(board)
    print(f"shape: {board.shape}")
    slice_func = lambda i: slice(max(i-1,0), i+2)
    edges = lambda board, ns, pos_i: np.r_[np.zeros(1),ns] if pos_i == 0 \
            else np.r_[ns, np.zeros(1)] if pos_i == board.shape[0]-1 \
            else ns
    c_func = lambda ns: ns[1]

    for i in range(10):
        history.append(board)
        board = get_next_board(board, rules, slice_func, edges, c_func)
    for b in history:
        print(b)

if __name__ == "__main__":
    __main__()
