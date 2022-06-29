from random import randint
import matplotlib.pyplot as plt

contour_cases = {
    0  : [],
    1  : [[[0.5, 0],[0, 0.5]]],
    2  : [[[1, 0.5],[0.5, 0]]],
    3  : [[[1, 0.5],[0, 0.5]]],
    4  : [[[1, 0.5],[0.5, 1]]],
    5  : [[[1, 0.5],[0.5, 0]],[[0, 0.5],[0.5, 1]]],
    6  : [[[0.5, 0],[0.5, 1]]],
    7  : [[[0, 0.5],[0.5, 1]]],
    8  : [[[0, 0.5],[0.5 , 1]]],
    9  : [[[0.5, 0],[0.5, 1]]],
    10 : [[[0.5, 0],[0, 0.5]],[[1, 0.5],[0.5, 1]]],
    11 : [[[1, 0.5],[0.5, 1]]],
    12 : [[[0, 0.5],[1, 0.5]]],
    13 : [[[0.5, 0],[1, 0.5]]],
    14 : [[[0.5, 0],[0, 0.5]]],
    15 : [],
}



def random_grid(size:tuple = (10,10), spread:tuple = (0,2)) -> list:
    return [[randint(*spread) for _ in range(size[0])] for _ in range(size[1])]


class MarchingSquares(object):
    """
    An object for a marching-squares implementation.

    
    """

    def __init__(self, grid:list, threshold:float = 1) -> None:

        self.threshold = threshold
        self.h = len(grid)
        self.w = len(grid[0])
        assert 1 < self.h and 1 < self.w  # We dont want any 1D grids

        self.grid = grid
        self.binary_grid = self.__threshold(self.grid)
        self.cells = self.__calc_cell_values(self.binary_grid)
        


    def __threshold(self, grid: list) -> list:
        """ Binarize the grid to 0 and 1 using a threshold. Threshold defaults to 1. """
        g = [[0 for _ in range(self.w)] for _ in range(self.h)]

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                g[i][j] = int(self.threshold < cell)            
        return g


    def __calc_cell_values(self, grid: list) -> list:
        """ 
        Every 2x2 block of cells in the binary image forms a contouring cell, so the whole image is 
        represented by a grid of such cells.
        Every cell is given a number between 0 and 15 corresponding to the neighbour configuration.
        Note that this grid of cells is one cell smaller in each direction than the original 2D field.
        
        Source: https://en.wikipedia.org/wiki/Marching_squares
        """

        cells = [[0 for _ in range(self.w-1)] for _ in range(self.h-1)]

        for y in range(self.h-1):
            for x in range(self.w-1):
                # Use 1 - x to invert 0 and 1 and use as a bitmask
                cells[y][x] = 8*(1-grid[y][x]) + 4*(1-grid[y][x+1]) + 1*(1-grid[y+1][x]) + 2*(1-grid[y+1][x+1])

        return cells


    def plot(self) -> None:
        h,w = self.h-1, self.w-1
        
        plt.figure(figsize=(7,7))
        plt.axes(xlim=(0, w), ylim=(0, h))

        for y in range(h):
            for x in range(w):
                for edge in contour_cases[self.cells[y][x]]:
                    plt.plot([edge[0][0]+x, edge[1][0]+x],[h+edge[0][1]-y-1, h+edge[1][1]-y-1], 'orange', zorder=1)
            
        plt.show()


