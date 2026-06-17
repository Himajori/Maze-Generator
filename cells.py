import random

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

def dfs_algo(cell, grid):
    unvisited = get_unvisted_neighbors(cell, grid)

    if not unvisited:
        return None

    direction = random.choice(list(unvisited.keys()))
    neighbor = unvisited[direction]

    remove_wall(cell, neighbor, direction)
    neighbor.visited = True

    return neighbor


def generate_maze(grid, start):
    stack = []

    start.visited =  True
    stack.append(start)

    while stack:
        # print(f"Stack: ",[(c.x, c.y)for c in stack])
        current = stack[-1]

        next_cell = dfs_algo(current, grid)
        if next_cell:
            stack.append(next_cell)
        else:
            stack.pop()

def all_cells_visited(grid):
    for row in grid:
        for cell in row:
            if not cell.visited:
                return False
    return True


def has_3x3_open(grid):
    height = len(grid)
    width = len(grid[0])

    for y in range(height - 2):
        for x in range(width - 2):
            if is_3x3_open(grid, x, y):
                return True
    return False

def is_3x3_open(grid, x, y):
    for dy in range(3):
        for dx in range(3):
            cell = grid[dy + y][dx + x]

            if dx < 2 and cell.walls["E"]:
                return False
            if dy < 2 and cell.walls["N"]:
                return False
    return True


def is_fully_closed(cell):
    return all(cell.walls.values())

grid = create_grid(3,3)
for row in grid:
    print([f"({c.x}, {c.y})" for c in row])

cell = grid[0][0]
neighbors = grid[0][1]

start = grid[0][0]
check = is_fully_closed(cell)
print("Check: ", check)
# pattern_42(grid)
generate_maze(grid, start)
print()
check = is_fully_closed(cell)
print("Check: ", check)
cell.walls["E"] = True
cell.walls["S"] = True
cell.walls["W"] = True
cell.walls["N"] = False
print()
check = is_fully_closed(cell)
print("Check: ", check)
