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
    s = round(W/n)
    i,j = 10,10
    for j,r in enumerate(board):
        for i,c in enumerate(r):
            x,y = i*s, (j*s) % H
            if c == 1:
                pygame.draw.rect(screen, white, pygame.Rect(x,y,s,s))

def __main__():
    #board, progress = cell_auta_1d(100, 182, mid=True)
    board, progress = conways_game_of_life(150, 150, rnd=0.1, state_dict=None)
    history = np.array([board])

    # graphics
    W,H = 1000, 1000
    pygame.init()
    screen = pygame.display.set_mode((W,H))

    history_bool = False
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
                    board = progress(board)
                    if history_bool:
                        history = np.r_[history, [board]]
                elif event.key == pygame.K_p:
                    play_bool = not play_bool
                elif event.key == pygame.K_ESCAPE:
                    loop_bool = False

        tf = tn - tp
        if play_bool and tf % spd == 1:
            tp = tn
            board = progress(board)
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
