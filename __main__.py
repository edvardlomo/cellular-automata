from logic import *
from boards import *
from collections import defaultdict
import numpy as np
import time
import pygame


black = (0,0,0)
white = (255,255,255)

def show(screen, W,H, board, cell_display):
    if len(board.shape) == 1:
        board = np.array([board])
    n = board.shape[1]
    s = round(W/n)
    for j,r in enumerate(board):
        for i,c in enumerate(r):
            x,y = i*s, (j*s) % H
            cell_display[c](x, y, s)
            #if c == 1:
            #    pygame.draw.rect(screen, white, pygame.Rect(x,y,s,s))

def __main__():
    #board, progress = cell_auta_1d(100, 182, mid=True)
    board, progress = conways_game_of_life(100, 100, state_dict=None, rnd=0.5)
    history = np.array([board])

    # graphics
    W,H = 1000, 1000
    pygame.init()
    screen = pygame.display.set_mode((W,H))

    # For mouse interaction
    if len(board.shape) >= 2:
        s = round(W/board.shape[1])
        calc_pos = lambda pos: (np.floor(pos[1]/s).astype('int'), np.floor(pos[0]/s).astype('int'))
    
    # Display cells
    cell_display = {0: (lambda x, y, s: None),
            1: (lambda x, y, s: pygame.draw.rect(screen, white, pygame.Rect(x,y,s,s))),
            2: (lambda x, y, s: pygame.draw.rect(screen, (0,0,255), pygame.Rect(x,y,s,s)))}


    history_bool = len(board.shape) == 1
    loop_bool = True
    play_bool = False
    tp = 0
    spd = 2
    acc = 1000
    left_mouse, right_mouse = False, False
    left_state, right_state = 1, 0
    mouse_sel = True
    key_state = [(pygame.K_0,0), (pygame.K_1,1),
            (pygame.K_2,2), (pygame.K_3,3),
            (pygame.K_4,4), (pygame.K_5,5),
            (pygame.K_6,6), (pygame.K_7,7),
            (pygame.K_8,8), (pygame.K_9,9),]
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
                elif event.key == pygame.K_SPACE:
                    mouse_sel = not mouse_sel
                for key, state in key_state:
                    if event.key == key:
                        if mouse_sel:
                            left_state = state
                        else:
                            right_state = state
                        break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    left_mouse = True
                if event.button == 3: # Right click
                    right_mouse = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Left click
                    left_mouse = False
                if event.button == 3: # Right click
                    right_mouse = False
                
        if left_mouse and right_mouse:
            pass
        elif left_mouse:
            pos = pygame.mouse.get_pos()
            pos = calc_pos(pos)
            board[pos] = left_state
        elif right_mouse:
            pos = pygame.mouse.get_pos()
            pos = calc_pos(pos)
            board[pos] = right_state

        tf = tn - tp
        if play_bool and tf % spd == 1:
            tp = tn
            board = progress(board)
            if history_bool:
                history = np.r_[history, [board]]

        screen.fill(black)
        if history_bool:
            show(screen, W,H, history, cell_display)
        else:
            show(screen, W,H, board, cell_display)
        pygame.display.update()

if __name__ == "__main__":
    __main__()
