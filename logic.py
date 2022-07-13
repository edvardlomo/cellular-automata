import numpy as np


def get_next_state(rules, c, ns):
    """Generates a state based c and ns and a list of rules"""
    if len(rules) == 0:
        return c
    if rules[0][0](c, ns):
        return rules[0][1]
    return get_next_state(rules[1:], c, ns)


def gen_pos(shape):
    """Return a generator that generates every position a board with the given shape."""
    if len(shape) == 1:
        return ((i,) for i in range(shape[0]))
    gen_subpos = gen_pos(shape[1:])
    return ((i, *subpos) for subpos in gen_subpos for i in range(shape[0]))


def get_next_board(board, rules, slice_func, edges, c_func):
    """
        1. Makes empty board, same size as previous board
        For every position of the board:
        2. Get neighbors using a slice function that returns a slice object. This step can be skipped, and neighborsthe neighbors are gotten from the edges function. This makes it possible to have neighbors be anything.
        3. Do edge cases with edges.
        4. Process neighbors in get_next_step, to get the next state for the cell
        end for loop and return the new board

        Input
            board: the current board with the cell states
            rules: see get_next_state
            slice_func: a function taking the same amount of arguments as there are dimensions of the board. Returns a slice object.
            edges: a function taking the board, neighbors, and the positions of the board. Returns a set of neighbors after handling edge cases.
            c_func: a function taking the neighbors as argument. Returns a state.
    """
    new_board = np.zeros(board.shape)
    for pos in gen_pos(board.shape):
        ns = board[slice_func(*pos)]
        ns = edges(board, ns, *pos)
        new_board[pos] = get_next_state(rules, c_func(ns), ns)
    return new_board.astype('int')
