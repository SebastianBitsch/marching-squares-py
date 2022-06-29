from MarchingSquares import MarchingSquares, random_grid


if __name__ == "__main__":

    N = 50
    grid = random_grid((N,N))

    ms = MarchingSquares(grid)
    ms.plot_polygons()
