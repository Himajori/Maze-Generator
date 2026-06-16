class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }


def create_grid(width: int, height:int):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)

    return grid

def get_neighbors(cell, grid):
    neighbors = {}
    width = len(grid[0])
    height= len(grid)
    x, y = cell.x, cell.y
    if y > 0:
        neighbors["N"] = grid[y - 1][x]
    if x < width -1:
        neighbors["E"] = grid[y][x + 1]
    if y < height - 1:
        neighbors["S"] = grid[y + 1][x]
    if x > 0:
        neighbors["W"] = grid[y][x - 1]

    return neighbors

OPPOSITE = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E"
}

def remove_wall(cell, neighbor, direction):
    cell.walls[direction] = False
    neighbor.walls[OPPOSITE[direction]] = False

def get_unvisted_neighbors(cell, grid):
    neighbors = get_neighbors(cell, grid)

    unvisted_neighbors = {}
    for dir in neighbors:
        neighbor = neighbors[dir]
        if not neighbor.visited:
            unvisted_neighbors[dir] = neighbor
    return unvisted_neighbors

grid = create_grid(3,3)
for row in grid:
    print([f"({c.x}, {c.y})" for c in row])


cell = grid[0][0]
neighbors = get_neighbors(cell, grid)

# for dir, nei in neighbors.items():
#     print(f"{dir}: ({nei.x}, {nei.y})")

unvisited = get_unvisted_neighbors(cell, grid)
for dir, nei in unvisited.items():
    print(f"{dir}: ({nei.x}, {nei.y})")
