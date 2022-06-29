from MarchingSquares import MarchingSquares, random_grid


if __name__ == "__main__":

    N = 20
    grid = random_grid((N,N))

    ms = MarchingSquares(grid)
    ms.plot()
