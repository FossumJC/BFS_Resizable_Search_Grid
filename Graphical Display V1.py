import random
import math
import time
import numpy as np
from matplotlib import pyplot as plot
from matplotlib import colors
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

tic = time.perf_counter()
# <--Initialize the Grid Data-->
Rows = 2000  # Total number of rows in the grid
Columns = 2000  # Total number of columns in the grid
d = np.zeros((Rows, Columns))  # Map data using a matrix structure

# White is an empty grid space = 0
# Black is a blocked grid space = 1
# Yellow is the start position grid space = 2
# Green is the goal position grid space = 3
# Blue is the shorted path from the start position to the goal position = 4
color_map = colors.ListedColormap(['white', 'black', 'yellow', 'green', 'blue'])  # Set the available colors of the plot
color_map_bounds = [0, 1, 2, 3, 4, 5]
norm = colors.BoundaryNorm(color_map_bounds, color_map.N)
d[0, 0] = 2  # Set the upper left corner the start position
d[Rows - 1, Columns - 1] = 3  # Set the lower right corner the goal position

plot.figure(figsize=(10, 10))  # Set the size of the figure when displayed
plot.pcolor(d, cmap=color_map, norm=norm, edgecolors='k',
            linewidth=1)  # Set the plot color map, edge colors and line width
C_Space = plot.gca()  # Get the current axes and call them the C_space
C_Space.set_ylim(C_Space.get_ylim()[::-1])  # Invert the Y-Axis to read from top to bottom
C_Space.xaxis.tick_top()  # Move the X-Axis to the top of the grid
C_Space.yaxis.tick_left()  # Make sure the Y-Axis is on the left of the grid

# Change major ticks to show every 1/10th of size
C_Space.xaxis.set_major_locator(MultipleLocator(Columns))
C_Space.yaxis.set_major_locator(MultipleLocator(Rows))


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
print("Number of Blocks: " + str(blocks))
print("Block size: " + str(block_size))

# <--Place random blocks along the diagonal (+/- 1 grid space) of grid if the grid has both axes larger than 2-->
if blocks < 2 and small is False:
    row_middle = math.ceil(Rows / 2)
    column_middle = math.ceil(Columns / 2)
    vertical_justify = random.randint(-1, 1)
    horizontal_justify = random.randint(-1, 1)
    row_block = row_middle + vertical_justify
    column_block = column_middle + horizontal_justify
    v_or_h = random.randint(0, 1)
    print("Home Block: [" + str(row_block - 1) + ", " + str(column_block - 1) + "]")
    if v_or_h == 0:
        print("Vertical")
        for i in range(block_size):
            print("i: " + str(i))
            try:
                # Catch the block from drawing over the goal position
                if row_block - i == Rows - 1 and column_block - 1 == Columns - 1:
                    d[row_block - block_size, column_block - 1] = 1
                    print("Goal Blocked from Row")
                    print("Blocking: [" + str(row_block - block_size) + "," + str(column_block - 1) + "]")
                # Catch the block from drawing over the start position
                elif row_block - i == 0 and column_block - 1 == 0:
                    d[row_block + 1, column_block - 1] = 1  # Old was +block_size
                    print("Start Blocked from Row")
                    print("Blocking: [" + str(row_block + 1) + "," + str(column_block - 1) + "]")
                else:
                    d[row_block - i, column_block - 1] = 1
                    print("Blocking: [" + str(row_block - i) + "," + str(column_block - 1) + "]")
            except IndexError:
                d[row_block - block_size, column_block - 1] = 1
                print("IndexError: Block moved back within Row range automatically")
                print("Blocking: [" + str(row_block - block_size) + "," + str(column_block - 1) + "]")
                pass
    else:
        print("Horizontal")
        for i in range(block_size):
            print("i: " + str(i))
            try:
                # Catch the block from drawing over the goal position
                if column_block - i == Columns - 1 and row_block - 1 == Rows - 1:
                    d[row_block - 1, column_block - block_size] = 1
                    print("Goal Blocked from Column")
                    print("Blocking: [" + str(row_block - 1) + "," + str(column_block - block_size) + "]")
                # Catch the block from drawing over the start position
                elif column_block - i == 0 and row_block - 1 == 0:
                    d[row_block - 1, column_block + 1] = 1  # Old was +block_size
                    print("Start Blocked from Column")
                    print("Blocking: [" + str(row_block - 1) + "," + str(column_block + 1) + "]")
                else:
                    d[row_block - 1, column_block - i] = 1
                    print("Blocking: [" + str(row_block - 1) + "," + str(column_block - i) + "]")
            except IndexError:
                d[row_block - 1, column_block - block_size] = 1
                print("IndexError: Block moved back within Column range automatically")
                print("Blocking: [" + str(row_block - 1) + "," + str(column_block - block_size) + "]")
                pass
elif small is False:
    pass

# <--Search in every direction: North South East West/Up Down Right Left using BFS-->
plot.pcolor(d, cmap=color_map, norm=norm, edgecolors='k',
            linewidth=1)  # Set the plot color map, edge colors and line width
plot.show()
toc = time.perf_counter()
print(f"Code ran in {toc-tic:0.4f} seconds")
