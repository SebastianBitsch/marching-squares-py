from MarchingSquares import MarchingSquares, random_grid

# Sample boards
from sample_boards import sample_grids

if __name__ == "__main__":

    N = [5, 10, 50, 100]

    # show sample grids
    for grid in sample_grids:
        ms = MarchingSquares(grid)

        ms.plot_grid()
        ms.plot_edges(show_grid=True)
        ms.plot_polygons(show_grid=True)
        ms.plot_polygons(show_grid=False)    

    # show random grids
    for n in N:
        grid = random_grid((n,n))
        ms = MarchingSquares(grid)

        ms.plot_grid()
        ms.plot_edges(show_grid=True)
        ms.plot_polygons(show_grid=True)
        ms.plot_polygons(show_grid=False)

