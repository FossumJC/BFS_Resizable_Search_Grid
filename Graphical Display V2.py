import random
import math
import time
import queue
import numpy as np
from matplotlib import pyplot as plot
from matplotlib import colors

# tic = time.perf_counter()
# <--Initialize the Grid Data-->
Rows = 1600  # Total number of rows in the grid
Columns = 1600  # Total number of columns in the grid
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

plot.figure(figsize=(12, 10))  # Set the size of the figure when displayed
gridMap = plot.imshow(d, cmap=color_map, interpolation='nearest', origin='upper', vmin=0, vmax=4, aspect='auto')
legend = plot.colorbar(gridMap, boundaries=color_map_bounds, ticks=[0, 1, 2, 3, 4])
legend.ax.set_yticklabels(["Free Space", "Blocked Space", "Start Position", "Goal Position", "Shortest Path"])
C_Space = plot.gca()  # Get the current axes and call them the C_space
C_Space.xaxis.tick_top()  # Move the X-Axis to the top of the grid


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
# blocks will be 2 grid spaces. Blcoks are also randomized to be drawn vertically or horizontally-->
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

# <--Search in every direction: North South East West/Up Down Right Left using BFS-->
visited_grid = set()  # Empty set (can be added to iteratively)
Q = queue.Queue(maxsize=0)  # Pythons queue data type
solution = {}  # An empty dictionary to be used later to verify shortest path
start = [0, 0]
goal = [Rows-1, Columns-1]
Q.put(start)
solution[start[0], start[1]] = start[0], start[1]

while Q.empty() is False:  # Exit while loop when the queue is empty (is equal to a length of zero)
    current = Q.get()  # Get the next entry in the queue and assign to current location
    while current[0] < 0 or current[1] < 0:
        current = Q.get()
    # print(current)
    # print(visited_grid)
    # time.sleep(0.5)

    try:
        # Check the cell diag-down-right from the current cell
        if d[current[0] + 1, current[1] + 1] != 1 and (current[0] + 1, current[1] + 1) not in visited_grid:
            # Check if "next" cell is wall
            if current[0] + 1 <= Rows and current[1] + 1 <= Columns:
                solution[current[0] + 1, current[1] + 1] = current[0], current[1]
                Q.put([current[0] + 1, current[1] + 1])
                visited_grid.add((current[0] + 1, current[1] + 1))

        # Check the cell down from the current cell
        if d[current[0] + 1, current[1]] != 1 and (current[0] + 1, current[1]) not in visited_grid:
            # Check if "next" cell is wall
            if current[0] + 1 <= Rows:
                solution[current[0] + 1, current[1]] = current[0], current[1]
                Q.put([current[0] + 1, current[1]])
                visited_grid.add((current[0] + 1, current[1]))

        # Check the cell right from the current cell
        if d[current[0], current[1] + 1] != 1 and (current[0], current[1] + 1) not in visited_grid:
            # Check if "next" cell is wall
            if current[1] + 1 <= Columns:
                solution[current[0], current[1] + 1] = current[0], current[1]
                Q.put([current[0], current[1] + 1])
                visited_grid.add((current[0], current[1] + 1))

        # Check the cell up from the current cell
        if d[current[0] - 1, current[1]] != 1 and (current[0] - 1, current[1]) not in visited_grid:
            # Check if "next" cell is wall
            if current[0] - 1 <= 0:
                solution[current[0] - 1, current[1]] = current[0], current[1]
                Q.put([current[0] - 1, current[1]])
                visited_grid.add((current[0] - 1, current[1]))

        # Check the cell left from the current cell
        if d[current[0], current[1] - 1] != 1 and (current[0], current[1] - 1) not in visited_grid:
            # Check if "next" cell is wall
            if current[1] - 1 <= 0:
                solution[current[0], current[1] - 1] = current[0], current[1]
                Q.put([current[0], current[1] - 1])
                visited_grid.add((current[0], current[1] - 1))
    # Catch if the cell is outside of the grid and do nothing
    except IndexError:
        pass

path = goal
print(len(solution))
while path != (start[0], start[1]):  # Exit loop when the current cell (path) is the start cell
    d[solution[path[0], path[1]]] = 4  # Identify the key value of solution [] as blue (path in graph)
    path = solution[path[0], path[1]]  # Value of old key now becomes the new key

# <--Display grid and solution path-->
d[0, 0] = 2  # Redraw the upper left corner as the start position
gridMap = plot.imshow(d, cmap=color_map, interpolation='nearest', origin='upper', vmin=0, vmax=4, aspect='auto')
plot.show()
# toc = time.perf_counter()
# print(f"Code ran in {toc-tic:0.4f} seconds")
