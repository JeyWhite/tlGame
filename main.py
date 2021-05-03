import numpy as np
import os
from msvcrt import getch

WALL: int = 10
EMPTY: int = 0
UNIT: int = 1
BOX: int = 2
POINT: int = 3
HOLD: int = -1
DONE: int = 5

LEFT = [0, -1]
RIGHT = [0, 1]
UP = [-1, 0]
DOWN = [1, 0]


def out_walls(level):
    for i in range(level.shape[0]):
        for j in range(level.shape[1]):
            if (i == 0 or j == 0) or (i == level.shape[0] - 1 or j == level.shape[1] - 1):
                level[i, j] = WALL
    return level


def get_pos(level):
    if UNIT in level:
        return np.argwhere(cur_level == UNIT)[0]
    else:
        return np.argwhere(cur_level == HOLD)[0]


def check_to_move(level: np.ndarray, direction, pos, r: int):
    if r > 2:
        return False
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    to_check = level[new_pos[0], new_pos[1]]
    if to_check == WALL:
        return False
    elif to_check == HOLD:
        return False
    elif to_check == POINT:
        return True
    elif to_check == EMPTY:
        return True
    elif to_check == BOX:
        return check_to_move(level, direction, new_pos, r + 1)
    elif to_check == DONE:
        return check_to_move(level, direction, new_pos, r + 1)


def move(level, direction, pos, r: int):
    if r > 2:
        return False
    new_pos = [pos[0] + direction[0], pos[1] + direction[1]]
    to_move = level[new_pos[0], new_pos[1]]
    moved = level[pos[0], pos[1]]
    if (moved, to_move) == (BOX, EMPTY):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (EMPTY, BOX)
    elif (moved, to_move) == (UNIT, BOX):
        level = move(level, direction, new_pos, r + 1)
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (EMPTY, UNIT)
    elif (moved, to_move) == (HOLD, BOX):
        level = move(level, direction, new_pos, r + 1)
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (POINT, UNIT)
    elif (moved, to_move) == (BOX, POINT):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (EMPTY, DONE)
    elif (moved, to_move) == (HOLD, POINT):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (POINT, HOLD)
    elif (moved, to_move) == (HOLD, EMPTY):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (POINT, UNIT)
    elif (moved, to_move) == (UNIT, EMPTY):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (EMPTY, UNIT)
    elif (moved, to_move) == (UNIT, POINT):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (EMPTY, HOLD)
    elif (moved, to_move) == (UNIT, DONE):
        level = move(level, direction, new_pos, r + 1)
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (EMPTY, HOLD)
    elif (moved, to_move) == (DONE, EMPTY):
        (level[pos[0], pos[1]], level[new_pos[0], new_pos[1]]) = (POINT, BOX)

    return level

    # if moved == BOX:
    #     level[pos[0], pos[1]] = EMPTY
    # elif moved == UNIT:
    #     level[pos[0], pos[1]] = EMPTY
    # elif moved == HOLD:
    #     level[pos[0], pos[1]] = POINT
    # elif moved == DONE:
    #     level[pos[0], pos[1]] = POINT
    #
    # if to_move == EMPTY:
    #     level[new_pos[0], new_pos[1]] = (UNIT if moved == HOLD else moved)
    #     return level
    # elif to_move == BOX:
    #     level = move(level, direction, new_pos, r + 1)
    #     level[new_pos[0], new_pos[1]] = POINT if moved == HOLD else moved
    #     return level
    # if to_move == POINT:
    #     level[new_pos[0], new_pos[1]] = (HOLD if moved == UNIT else (DONE if moved == BOX else moved))
    #     return level


def game_render(level):
    symbols = {
        10: "█",
        0: " ",
        1: "X",
        2: "B",
        3: "×",
        -1: "Y",
        5: "D"
    }

    for i in symbols.keys():
        level[level == i] = ord(symbols[i])
    for i in range(level.shape[0]):
        for j in range(level.shape[1]):
            print(chr(level[i, j]), end="")
        print("")


def get_button():
    buttons = {
        72: UP,
        75: LEFT,
        80: DOWN,
        77: RIGHT
    }
    while True:
        key = ord(getch())
        if key in [72, 77, 80, 75]:
            # print(key)
            return buttons[key]


def game_cycle(level):
    game_on = True

    while game_on:
        game_render(level.copy())

        command = get_button()
        os.system("cls")

        cur_pos = get_pos(level)
        if check_to_move(level, command, cur_pos, 1):
            level = move(level, command, cur_pos, 1)
        game_on = BOX in level
    return print("Win")


if __name__ == '__main__':
    cur_level = np.array([
        [10, 10, 10, 10, 10, 10],
        [10, 0, 0, 0, 0, 10],
        [10, 3, 0, 2, 1, 10],
        [10, 0, 0, 0, 0, 10],
        [10, 10, 10, 10, 10, 10]

    ])
    os.system("cls")
    game_cycle(cur_level)
    # print(cur_level)
    # print(type(cur_level))
    # os.system("cls")
    # print(np.where(cur_level == UNIT))
    # print()
