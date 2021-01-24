import re
import keras
import numpy as np
# from main.py import load_map


def print_grid(grid, new_line=True):
    if new_line: print("")
    print("[")
    for row in grid:
        print(f"  {row},")
    print("]")


def load_map(map_path):
    mapping = {}

    with open(map_path) as f:
        for line in f.read().split("\n")[:-1]:
            split = line.split()
            mapping[int(split[0])] = int(split[1])

    return mapping


# import model
# https://stackoverflow.com/questions/43017017/keras-model-predict-for-a-single-image

model = keras.models.load_model('data/model_letters_e20_2')
mapping = load_map("data/emnist-letters-mapping.txt")

'''
grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    ]
'''

# could use a dict with a tuple as the key

cols = rows = 28

grid = [[0 for i in range(cols)] for i in range(rows)]

start = 100
end = 200
cell_width = cell_height = 10

print_grid(grid, new_line=False)
coords = input(
    "What are the coordinates of the pixel you would like to activate? ")
while coords:
    if coords == "clear":
        for row in grid:
            for pixel in row:
                pixel = 0
    else:
        match = re.match(r"\((\d+), (\d+)\)", coords)
        if match:
            #print(match, match[0], match[1], match[2])

            #print(re.match("test", "test_string"), bool(re.match("test", "test_string")))
            #print("Will run some code when I get around to coding it...")

            # x = int(coords[1])
            # y = int(coords[4])
            x = int(match[1])
            y = int(match[2])
            if (x >= 0 and x < cols) and (y >= 0 and y < rows):
                grid[y][x] = 1
                print(f"Set {coords} to 1")
            else:
                print("Coordinate(s) out of bounds")
        else:
            print("Please enter a valid input, e.g. (0, 1)")

    print_grid(grid)

    # format grid like EMNIST data
    #char = np.asarray(grid)

    # print(char.shape)
    # print(char)

    # char = char.reshape([1, 3, 3, 1])
    # # should be (1, 28, 28, 1)

    # print("")
    # print(char.shape)
    # print(char)

    # char = char.transpose()

    # print("")
    # print(char.shape)
    # print(char)
    # print(char.reshape([3, 3]))

    char = np.asarray(grid).reshape([1, cols, rows, 1]).transpose()

    #print("")
    #print(char.reshape([cols, rows]))

    print("")
    prediction = np.argmax(model.predict(char), axis=1)
    prediction = chr(mapping[int(prediction)])
    print(prediction)

    coords = input(
        "What are the coordinates of the pixel you would like to activate? ")


# subtract the starting x value from the input x value,
# then floor-divide by the width to get the position of the cell.
# then, subtract 1 to convert to an index.
