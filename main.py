from MarchingSquares import MarchingSquares, random_grid


if __name__ == "__main__":

    N = 51
    grid = random_grid((N,N))

    ms = MarchingSquares(grid)
    ms.plot_edges(plot_grid=True)
