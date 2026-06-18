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


def close_cell(grid, x, y):
    cell = grid[y][x]
    cell.visited = True


def draw_4(grid, x, y):
    coords = [
        (0, 0),
        (0, 1),
        (0, 2), (1, 2), (2, 2),
                        (2, 3),
                        (2, 4)
    ]

    for dx, dy in coords:
        close_cell(grid, x + dx, y + dy)


def draw_2(grid, x, y):
    coords = [
        (0, 0), (1, 0), (2,0),
                        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4)                
    ]

    for dx, dy in coords:
        close_cell(grid, x + dx, y + dy)


def place_42_pattern(grid):
    height = len(grid)
    width = len(grid[0])

    pattern_width = 7
    pattern_height = 5

    if width < 11 or height < 9:
        print("Error: maze too small for 42 pattern")
        return False
    
    start_x = (width - pattern_width) // 2
    start_y = (height - pattern_height) // 2

    draw_4(grid, start_x, start_y)
    draw_2(grid, start_x + 4, start_y)

    return True


WALL_BITS = {
    "N": 1,
    "E": 2,
    "S": 4,
    "W": 8
}

def encoded_cell(cell):
    value = 0

    for dir, bit in WALL_BITS.items():
        if cell.walls[dir]:
            value |= bit
    
    return value


grid = create_grid(11, 9)
for row in grid:
    print([f"({c.x}, {c.y})" for c in row])

cell = grid[0][0]
neighbor = grid[0][1]
check_cell = grid[8][2]
start = grid[0][0]

check = is_fully_closed(cell)
print("Check: ", check)
place_42_pattern(grid)
generate_maze(grid, start)
print()
# if place_42_pattern(grid):
#     print("Is goood")

value = encoded_cell(cell)
print(cell.walls)
print(value)