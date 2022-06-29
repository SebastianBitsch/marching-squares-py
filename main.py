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

grid = [
    [1,1,1,1,1],
    [1,2,1,2,1],
    [1,1,2,3,1],
    [1,2,1,2,1],
    [1,1,1,1,1]
    ]

def threshold(grid: list, threshold:float=1) -> list:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            grid[i][j] = int(threshold < cell)            
    return grid


def calc_cells(grid: list) -> list:
    n,m = len(grid)-1, len(grid[0])-1
    cells = [[0 for _ in range(n)] for _ in range(m)]

    for y in range(n):
        for x in range(m):
            # Use 1 - x to invert 0 and 1
            cells[y][x] = 8*(1-grid[y][x]) + 4*(1-grid[y][x+1]) + 1*(1-grid[y+1][x]) + 2*(1-grid[y+1][x+1])

    return cells


if __name__ == "__main__":
    grid = threshold(grid)
    cells = calc_cells(grid)

    n,m = len(grid)-1, len(grid[0])-1
    
    # fig, ax = plt.subplots()

    # # ax.add_patch(p)
    # ax.set_xlim([0,n])
    # ax.set_ylim([0,m])
    plt.figure(figsize=(7,7))
    plt.axes(xlim=(0, n), ylim=(0, m))

    for y in range(n):
        for x in range(m):
            for edge in contour_cases[cells[y][x]]:
                plt.plot([edge[0][0]+x, edge[1][0]+x],[m+edge[0][1]-y-1, m+edge[1][1]-y-1], 'orange', zorder=1)
        
    plt.show()

