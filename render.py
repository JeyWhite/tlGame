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