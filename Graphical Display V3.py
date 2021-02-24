import random
import math
import time
import queue
import numpy as np
from matplotlib import pyplot as plot
from matplotlib import colors
from matplotlib.ticker import MultipleLocator

# tic = time.perf_counter()  # Timer for testing part one
# <--Initialize the Grid Data-->
Rows = 150  # Total number of rows in the grid
Columns = 150  # Total number of columns in the grid
d = np.zeros((Rows, Columns))  # Map data using a matrix structure

# White is an empty grid space = 0
# Black is a blocked grid space = 1
# Yellow is the start position grid space = 2
# Green is the goal position grid space = 3
# Blue is the shorted path from the start position to the goal position = 4
color_map = colors.ListedColormap(['white', 'black', 'yellow', 'green', 'blue'])  # Set the available colors of the plot
color_map_bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = colors.BoundaryNorm(color_map_bounds, color_map.N)
d[0, 0] = 2  # Set the upper left corner the start position
d[Rows - 1, Columns - 1] = 3  # Set the lower right corner the goal position


# <--Initialize the plot information-->
plot.figure(figsize=(12, 10))  # Set the size of the figure when displayed
gridMap = plot.imshow(d, cmap=color_map, interpolation='nearest', origin='upper', vmin=0, vmax=4)
legend = plot.colorbar(gridMap, boundaries=color_map_bounds, ticks=[0, 1, 2, 3, 4])
legend.ax.set_yticklabels(["Free Space", "Blocked Space", "Start Position", "Goal Position", "Shortest Path"])
C_Space = plot.gca()  # Get the current axes and call them the C_space
C_Space.xaxis.tick_top()  # Move the X-Axis to the top of the grid
# Show the size of the grid columns (user Column input verification of correct free space within the grid)
C_Space.xaxis.set_major_locator(MultipleLocator(Columns+1))
# Show the size of the grid rows (user Row input verification of correct free space within the grid)
C_Space.yaxis.set_major_locator(MultipleLocator(Rows+1))

# <--Check the size of the grid to determine the method of creating blocks-->
if Rows == 2:
    twoRows = True
else:
    twoRows = False
if Columns == 2 and twoRows is False:
    twoColumns = True
else:
    twoColumns = False

# <--Create a minimum of one grid that is blocked and declare 'small' grid-->
if twoRows is True or twoColumns is True:
    small = True
    random.seed(int(time.time()))
    if random.randint(0, 1) == 0:
        d[1, 0] = 1
    else:
        d[0, 1] = 1
else:
    small = False

diagonal = min(Rows, Columns)  # Find the minimum number of grid space (width or length)
if diagonal == 3:
    block_size = 2  # If grid space minimum is 3, set the block size to 2 grid spaces so there is always a solution
else:
    block_size = 3  # Set the block size to the standard 3 grid spaces
# If the minimum number of grid spaces is greater than 10, add one more random block per additional 10 grid spaces
blocks = math.ceil((diagonal / 15))

# <--Place random blocks along the diagonal with +/- 1 or 0 both horizontally and vertically from the middle of the 3
# blocked grid spaces if the grid has both axes larger than 2. If the grid is smaller than 4 rows or columns,
# blocks will be 2 grid spaces. Blocks are also randomized to be drawn vertically or horizontally-->
if blocks < 2 and small is False:
    row_middle = math.ceil(Rows / 2)
    column_middle = math.ceil(Columns / 2)
    vertical_justify = random.randint(-1, 1)
    horizontal_justify = random.randint(-1, 1)
    row_block = row_middle + vertical_justify
    column_block = column_middle + horizontal_justify
    v_or_h = random.randint(0, 1)
    if v_or_h == 0:
        # Drawing the block vertically
        for i in range(block_size):
            try:
                # Catch the block from drawing over the goal position
                if row_block - i == Rows - 1 and column_block - 1 == Columns - 1:
                    d[row_block - block_size, column_block - 1] = 1
                # Catch the block from drawing over the start position
                elif row_block - i == 0 and column_block - 1 == 0:
                    d[row_block + 1, column_block - 1] = 1
                else:
                    d[row_block - i, column_block - 1] = 1
            # Catch the block being drawn outside of the grid boundary
            except IndexError:
                d[row_block - block_size, column_block - 1] = 1
    else:
        # Drawing the block horizontally
        for i in range(block_size):
            try:
                # Catch the block from drawing over the goal position
                if column_block - i == Columns - 1 and row_block - 1 == Rows - 1:
                    d[row_block - 1, column_block - block_size] = 1
                # Catch the block from drawing over the start position
                elif column_block - i == 0 and row_block - 1 == 0:
                    d[row_block - 1, column_block + 1] = 1
                else:
                    d[row_block - 1, column_block - i] = 1
            # Catch the block being drawn outside of the grid boundary
            except IndexError:
                d[row_block - 1, column_block - block_size] = 1
elif small is False:
    for j in range(blocks):
        row_middle = math.floor(Rows / (blocks + 1)) * (j+1)
        column_middle = math.floor(Columns / (blocks + 1)) * (j+1)
        vertical_justify = random.randint(-1, 1)
        horizontal_justify = random.randint(-1, 1)
        row_block = row_middle + vertical_justify
        column_block = column_middle + horizontal_justify
        v_or_h = random.randint(0, 1)
        if v_or_h == 0:
            # Drawing the block vertically
            for i in range(block_size):
                try:
                    # Catch the block from drawing over the goal position
                    if row_block - i == Rows - 1 and column_block - 1 == Columns - 1:
                        d[row_block - block_size, column_block - 1] = 1
                    # Catch the block from drawing over the start position
                    elif row_block - i == 0 and column_block - 1 == 0:
                        d[row_block + 1, column_block - 1] = 1
                    else:
                        d[row_block - i, column_block - 1] = 1
                # Catch the block being drawn outside of the grid boundary
                except IndexError:
                    d[row_block - block_size, column_block - 1] = 1
        else:
            # Drawing the block horizontally
            for i in range(block_size):
                try:
                    # Catch the block from drawing over the goal position
                    if column_block - i == Columns - 1 and row_block - 1 == Rows - 1:
                        d[row_block - 1, column_block - block_size] = 1
                    # Catch the block from drawing over the start position
                    elif column_block - i == 0 and row_block - 1 == 0:
                        d[row_block - 1, column_block + 1] = 1
                    else:
                        d[row_block - 1, column_block - i] = 1
                # Catch the block being drawn outside of the grid boundary
                except IndexError:
                    d[row_block - 1, column_block - block_size] = 1

# <-- Place random blocks anywhere in the grid except within three grid spaces of the start or goal position-->
if small is False:
    fill = (d == 1).sum()
    fullness = fill/(Rows * Columns)
    row_no_go_list = [*range(0, Rows, 1)]
    column_no_go_list = [*range(0, Columns, 1)]

    while fullness < 0.25:
        new_block = [np.random.randint(Rows), np.random.randint(Columns)]
        if (new_block[0] in row_no_go_list[0:int(Rows*0.1)] and new_block[1] in column_no_go_list[0:int(Columns*0.1)]) or (new_block[0] in row_no_go_list[Rows-int(Rows*0.1):Rows] and new_block[1] in column_no_go_list[Columns-int(Columns*0.1):Columns]):
            continue
        d[new_block[0], new_block[1]] = 1
        fill = (d == 1).sum()
        fullness = fill / (Rows * Columns)

# <--Create walls to bound internal grid-->
horizontal_wall = np.ones((1, Columns))
vertical_wall = np.ones((Rows + 2, 1))
d = np.vstack((horizontal_wall, d, horizontal_wall))
d = np.hstack((vertical_wall, d, vertical_wall))


# <--Search in every direction: North South East West/Up Down Right Left using BFS-->
visited_grid = set()  # Empty set (can be added to iteratively)
Q = queue.Queue(maxsize=0)  # Pythons queue data type
solution = {}  # An empty dictionary to be used later to verify shortest path
start = [1, 1]
goal = [Rows, Columns]
Q.put(start)
solution[start[0], start[1]] = start[0], start[1]

while Q.empty() is False:  # Exit while loop when the queue is empty (is equal to a length of zero)
    current = Q.get()  # Get the next entry in the queue and assign to current location

    try:
        # Check the cell down from the current cell
        if d[current[0] + 1, current[1]] != 1 and (current[0] + 1, current[1]) not in visited_grid:
            solution[current[0] + 1, current[1]] = current[0], current[1]
            Q.put([current[0] + 1, current[1]])
            visited_grid.add((current[0] + 1, current[1]))

        # Check the cell right from the current cell
        if d[current[0], current[1] + 1] != 1 and (current[0], current[1] + 1) not in visited_grid:
            solution[current[0], current[1] + 1] = current[0], current[1]
            Q.put([current[0], current[1] + 1])
            visited_grid.add((current[0], current[1] + 1))

        # Check the cell up from the current cell
        if d[current[0] - 1, current[1]] != 1 and (current[0] - 1, current[1]) not in visited_grid:
            solution[current[0] - 1, current[1]] = current[0], current[1]
            Q.put([current[0] - 1, current[1]])
            visited_grid.add((current[0] - 1, current[1]))

        # Check the cell left from the current cell
        if d[current[0], current[1] - 1] != 1 and (current[0], current[1] - 1) not in visited_grid:
            solution[current[0], current[1] - 1] = current[0], current[1]
            Q.put([current[0], current[1] - 1])
            visited_grid.add((current[0], current[1] - 1))
    # Catch if the cell is outside of the grid and do nothing
    except IndexError:
        pass
    visited_grid.add((current[0], current[1]))

# <--Trace back the optimal path-->
path = goal
if (Rows, Columns) in solution:
    plot.title("Goal Position Found: Solution Path Displayed")
    while path != (start[0], start[1]):  # Exit loop when the current cell (path) is the start cell
        d[solution[path[0], path[1]]] = 4  # Identify the key value of solution [] as blue (path in graph)
        path = solution[path[0], path[1]]  # Value of old key now becomes the new key
else:
    plot.title("Goal Position Blocked, No Solution Path Found")


# <--Display grid and solution path-->
d[1, 1] = 2  # Redraw the upper left corner as the start position as it gets drawn over in the
gridMap = plot.imshow(d, cmap=color_map, interpolation='nearest', origin='upper', vmin=0, vmax=4)
# toc = time.perf_counter()  # Timer for testing part two
# print(f"Code ran in {toc-tic:0.4f} seconds")  # Display timing results
plot.show()
