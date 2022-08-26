from MarchingSquares import MarchingSquares, random_grid

# Sample boards
from sample_boards import sample_grids

if __name__ == "__main__":

    N = [5, 10, 25, 50]


    # show premade sample grids
    for grid in sample_grids:
        ms = MarchingSquares(grid)

        ms.plot_grid()
        ms.plot_edges()
        ms.plot_polygons()
        ms.plot_polygons(show_grid=False)    

    # show random grids
    for n in N:
        grid = random_grid((n,n))
        ms = MarchingSquares(grid)

        ms.plot_grid()
        ms.plot_edges()
        ms.plot_polygons()
        ms.plot_polygons(show_grid=False)

