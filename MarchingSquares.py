from functools import reduce
from random import randint
from math import inf
import matplotlib.pyplot as plt


def random_grid(size:tuple = (10,10), num_range:tuple = (0,1)) -> list:
    """
    Generate a random grid of ints at a given ``size``. The numbers will lie within the given ``num_range``
    """
    return [[randint(*num_range) for _ in range(size[0])] for _ in range(size[1])]


class MarchingSquares(object):
    """
    An object for a marching-squares implementation.
    """

    def __init__(self, grid:list, lower_threshold:float = 0.5, upper_threshold:float = inf) -> None:
        """
        A marching square implementation that takes a 2D grid of values to form the grid around.

        Parameters
        ----------
        grid, list
            The grid of values to create marching squares from
        
        lower_threshold, float (optional)
            The lower value of values in the grid when binarizing the grid, all values below 
            this threshold will be set to zero

        upper_threshold, float (optional)
            The upper value to use when binarizing the grid. Default to zero, meaning no upper
            threshold will be set. Can be lowered to ensure only a band of values are binarized to 1.
        """

        # Only 2D grids with more than 1 value are valid - TODO: doesnt catch 3D list
        assert isinstance(grid, list) and 1 < len(grid), "'grid' was not a list with more than one element"
        assert reduce(lambda a,b : isinstance(b,list) and a, grid, True), "Not all elements in 'grid' were lists"
        assert reduce(lambda a,b : 1 < len(b) and a, grid, True), "Not all sublists had more than one element"

        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold

        self.h= len(grid)
        self.w = len(grid[0])
        self.N = self.w * self.h

        self.grid = grid
        self.binary_grid = self.__binarize(self.grid)
        self.cells = self.__calc_cell_values(self.binary_grid)
        

    def __binarize(self, grid: list) -> list:
        """ Binarize the grid to 0 and 1 using a threshold. Threshold defaults to 0.5. """
        g = [[0 for _ in range(self.w)] for _ in range(self.h)]

        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                g[x][y] = int(self.lower_threshold <= cell and cell <= self.upper_threshold)            
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


    def plot_polygons(self, fill:bool = True, show_grid:bool = True, edge_color:str = 'orange', fill_color:str = 'orange', fig_size:tuple = (7,7)) -> None:
        """
        Plot the polygons of the marching squares sequence.

        Parameters
        ----------
        
        fill, bool (optional)
            Boolean indication of whether to fill the polygons
        
        show_grid, bool (optional)
            Whether to show the grid points given, defaults to true
        
        edge_color, str (optional)
            The color of the edges to draw, defaults to orange
        
        fill_color, str (optional)
            The color to fill the polygons with, defaults to orange
        
        fig_size, tuple (optional)
            The size of the figure to draw, defaults to (7,7)
        """

        h,w = self.h-1, self.w-1
        
        plt.figure(figsize=fig_size)
        plt.axes(xlim=(0, w), ylim=(0, h))

        plt.title(f"N={self.N}", loc='left')
        plt.title("Marching Squares ", loc='center', fontweight='bold')
        
        if show_grid:
            self.__show_grid()

        for y in range(h):
            for x in range(w):
                for polygon in contour_polygons[self.cells[y][x]]:

                    points = [[x0+x, h-y-1+y0] for (x0,y0) in polygon]
                    
                    p = plt.Polygon(points, edgecolor=edge_color, facecolor=fill_color, fill=fill)
                    plt.gca().add_patch(p)
            
        plt.show()


    def plot_edges(self, show_grid:bool = True, edge_color:str = 'orange', fig_size:tuple = (7,7)) -> None:
        """ 
        Plot the outer edges of the resulting marching squares sequence 

        Parameters
        ----------
        show_grid, bool (optional)
            Whether to show the grid points given, defaults to true
        
        edge_color, str (optional)
            The color of the edges to draw, defaults to orange
        
        fig_size, tuple (optional)
            The size of the figure to draw, defaults to (7,7)
        """
        
        h,w = self.h-1, self.w-1
        
        plt.figure(figsize=fig_size)
        plt.axes(xlim=(0, w), ylim=(0, h))

        plt.title(f"N={self.N}", loc='left')
        plt.title("Marching Squares ", loc='center', fontweight='bold')
        
        if show_grid:
            self.__show_grid()

        for y in range(h):
            for x in range(w):

                cell_val = self.cells[y][x]
                for edge in contour_edges[cell_val]:
                    plt.plot([edge[0][0]+x, edge[1][0]+x],[h+edge[0][1]-y-1, h+edge[1][1]-y-1], color=edge_color, zorder=1)
        
        plt.show()


    def plot_grid(self, point_color:str = 'black', fig_size:tuple = (7,7)) -> None:
        """ 
        Plot the grid points in a plot with a color, title and size
        
        Parameters
        ----------

        point_color, (optional)
            The color in which to plot the points, defaults to black
        
        fig_size, tuple (optional)
            The size of the figure to draw, defaults to (7,7)
        """

        h,w = self.h-1, self.w-1
        
        plt.figure(figsize=fig_size)
        plt.axes(xlim=(0, w), ylim=(0, h))

        plt.title(f"N={self.N}", loc='left')
        plt.title("Marching Squares ", loc='center', fontweight='bold')
        
        self.__show_grid(point_color)
        plt.show()


    def __show_grid(self, color:str = 'black') -> None:
        """ Helper function to plot the individual points in the grid """

        for y in range(self.h):
            for x in range(self.w):

                if self.binary_grid[y][x]:
                    plt.plot([x],[self.h-y-1], marker='.', color=color, markersize=4)




contour_edges = {
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

contour_polygons = {
    0  : [[[0,0],[1,0],[1,1],[0,1]]],
    1  : [[[0.5, 0],[1,0],[1,1],[0,1],[0, 0.5]]],
    2  : [[[1, 0.5],[1,1],[0,1],[0,0],[0.5, 0]]],
    3  : [[[1, 0.5],[1,1],[0,1],[0, 0.5]]],
    4  : [[[1, 0.5],[0.5, 1],[0,1],[0,0],[1,0]]],
    5  : [[[1, 0.5],[0.5, 0],[1,0]],[[0, 0.5],[0.5, 1],[0,1]]],
    6  : [[[0.5, 0],[0.5, 1],[0,1],[0,0]]],
    7  : [[[0, 0.5],[0.5, 1],[0,1]]],
    8  : [[[0.5, 1],[0, 0.5],[0,0],[1,0],[1,1]]],
    9  : [[[0.5, 1],[0.5, 0],[1,0],[1,1]]],
    10 : [[[0.5, 0],[0, 0.5],[0,0]],[[1, 0.5],[0.5, 1],[1,1]]],
    11 : [[[0.5, 1],[1, 0.5],[1,1]]],
    12 : [[[1, 0.5],[0, 0.5],[0,0],[1,0]]],
    13 : [[[1, 0.5],[0.5, 0],[1,0]]],
    14 : [[[0.5, 0],[0, 0.5],[0,0]]],
    15 : [],
}
