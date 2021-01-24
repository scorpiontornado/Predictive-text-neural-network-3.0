cols = rows = 10
cell_width = cell_height = 10
start_x = start_y = 100
end_x = start_x + cols * cell_width  # should equal 200 for this example
end_y = start_y + rows * cell_height

print(start_x + cols * cell_width == 200)  # should be the same as end, 200

# subtract the starting x value from the input x value,
# then floor-divide by the width to get the position of the cell.

input_x = int(input("X coordinate of your 'click': "))
x = (input_x - start_x) // cell_width
if x >= cols:
    x = cols - 1

print(x)
