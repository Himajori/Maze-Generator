import random
from collections import deque


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


def create_grid(width: int, height: int):
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
    height = len(grid)
    x, y = cell.x, cell.y
    if y > 0:
        neighbors["N"] = grid[y - 1][x]
    if x < width - 1:
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

    start.visited = True
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
        (0, 0), (1, 0), (2, 0),
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


def encoded_grid(grid):
    lines = []
    for row in grid:
        line = ""
        for cell in row:
            encoded = encoded_cell(cell)
            line += format(encoded, "X")
        lines.append(line)

    return lines


def write_maze(file, grid):
    lines = encoded_grid(grid)
    for line in lines:
        file.write(line + "\n")


def write_entry_exit_(file, entry, exit_):
    file.write(f"{entry[0]}, {entry[1]}\n")
    file.write(f"{exit_[0]}, {exit_[1]}\n")


def write_output(filename, grid, entry, exit_, path):
    with open(filename, "w") as file:
        write_maze(file, grid)
        file.write("\n")
        write_entry_exit_(file, entry, exit_)
        file.write("\n")
        file.write(" ".join(path) + "\n")


DIRECTION = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0)
}


def can_move(grid, x, y, direction):
    cell = grid[y][x]

    if cell.walls[direction]:
        return False

    return True


def bfs_algo(grid, entry, exit_):
    queue = deque()
    visited = set()
    parent = {}

    queue.append(entry)
    visited.add(entry)

    while queue:
        x, y = queue.popleft()

        if (x, y) == exit_:
            return parent

        for d in DIRECTION:
            if can_move(grid, x, y, d):
                dx, dy = DIRECTION[d]
                nx, ny = x + dx, y + dy

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = ((x, y), d)
                    queue.append((nx, ny))
    return None


def reconstruct_path(parent, entry, exit_):
    path = []
    current = exit_

    while current != entry:
        prev, direction = parent[current]
        path.append(direction)
        current = prev

    path.reverse()
    return path


def shortest_path(grid, entry, exit_):
    parent = bfs_algo(grid, entry, exit_)

    if parent is None:
        return []
    return reconstruct_path(parent, entry, exit_)


def path_to_coords(entry, path):
    coords = [entry]
    x, y = entry

    for d in path:
        dx, dy = DIRECTION[d]
        x += dx
        y += dy
        coords.append((x, y))

    return coords


# grid = create_grid(20, 15)
grid = create_grid(3, 3)
for row in grid:
    print([f"({c.x}, {c.y})" for c in row])

cell = grid[0][0]
neighbor = grid[0][1]
# check_cell = grid[8][2]
start = grid[0][0]

# check = is_fully_closed(cell)
# print("Check: ", check)
# place_42_pattern(grid)
generate_maze(grid, start)
print()

# path = ["E", "S", "E", "E", "N", "E", "S", "W"]
# write_output("test.txt", grid, (0,0), (19,14), path)
# result = bfs_algo(grid, (0, 0), (2, 2))
path = shortest_path(grid, (0, 0), (2, 2))
print(path)
coord = path_to_coords((0, 0), path)
print(coord)
