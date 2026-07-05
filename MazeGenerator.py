import random
from collections import deque


class MazeGenerator():
    def __init__(self, width, height, entry, exit_,
                 perfect, output_file, seed=None):
        self.width = width
        self.height = height
        self.exit_ = exit_
        self.entry = entry
        self.perfect = perfect
        self.output_file = output_file
        self.seed = seed
        self.opposite = {
            "N": "S",
            "E": "W",
            "S": "N",
            "W": "E"
        }
        self.wall_bits = {
            "N": 1,
            "E": 2,
            "S": 4,
            "W": 8
        }
        self.directions = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0)
        }
        # Store all maze settings and build direction/wall lookup tables

    class Cell:
        # A single grid cell — tracks its position, visited state,
        # and which of its 4 walls (N/E/S/W) are still up
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
<<<<<<< HEAD:cells.py
=======
    # Build a 2D list (height x width) of Cell objects, all walls up
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py

    def create_grid(self):
        grid = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(MazeGenerator.Cell(x, y))
            grid.append(row)

        return grid

<<<<<<< HEAD:cells.py
=======
    # Return existing adjacent cells as {direction: cell}
    # Only includes directions that are inside the grid bounds
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def get_neighbors(self, cell, grid):
        neighbors = {}
        width = self.width
        height = self.height
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

<<<<<<< HEAD:cells.py
=======
    # Remove the wall between two adjacent cells on both sides
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def remove_wall(self, cell, neighbor, direction):
        cell.walls[direction] = False
        neighbor.walls[self.opposite[direction]] = False

<<<<<<< HEAD:cells.py
=======
    # Filter get_neighbors() to only cells not yet visited by DFS
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def get_unvisted_neighbors(self, cell, grid):
        neighbors = self.get_neighbors(cell, grid)

        unvisted_neighbors = {}
        for dir in neighbors:
            neighbor = neighbors[dir]
            if not neighbor.visited:
                unvisted_neighbors[dir] = neighbor

        return unvisted_neighbors

<<<<<<< HEAD:cells.py
=======
    # Run iterative DFS from grid[0][0] using an explicit stack
        # Keeps carving until every reachable cell has been visited
        # Cells pre-marked visited (42 pattern) are skipped automatically
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def dfs_algo(self, cell, grid):
        unvisited = self.get_unvisted_neighbors(cell, grid)

        if not unvisited:
            return None

        direction = random.choice(list(unvisited.keys()))
        neighbor = unvisited[direction]

        self.remove_wall(cell, neighbor, direction)
        neighbor.visited = True

        return neighbor

    def generate_maze(self, grid):
        # Run iterative DFS from grid[0][0] using an explicit stack
        # Keeps carving until every reachable cell has been visited
        stack = []
        start = grid[0][0]

        start.visited = True
        stack.append(start)

        while stack:
            # print(f"Stack: ",[(c.x, c.y)for c in stack])
            current = stack[-1]

            next_cell = self.dfs_algo(current, grid)
            if next_cell:
                stack.append(next_cell)
            else:
                stack.pop()

<<<<<<< HEAD:cells.py
=======
    # Return True if every cell in the grid has been visit
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def all_cells_visited(self, grid):
        for row in grid:
            for cell in row:
                if not cell.visited:
                    return False
        return True

<<<<<<< HEAD:cells.py
=======
    # Scan the whole grid for any 3x3 block that is fully open
    # The maze constraint forbids corridors wider than 2 cells
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def has_3x3_open(self, grid):
        height = self.height
        width = self.width

        for y in range(height - 2):
            for x in range(width - 2):
                if self.is_3x3_open(grid, x, y):
                    return True
        return False

<<<<<<< HEAD:cells.py
=======
    # Check if the specific 3x3 block starting at (x,y) has no
    # internal East or South walls (fully open area)
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def is_3x3_open(self, grid, x, y):
        for dy in range(3):
            for dx in range(3):
                cell = grid[dy + y][dx + x]

                if dx < 2 and cell.walls["E"]:
                    return False
                if dy < 2 and cell.walls["N"]:
                    # duhet te jete cells.walls["S"] ketu apo jooo ?
                    return False
        return True

<<<<<<< HEAD:cells.py
=======
    # Return True if all 4 walls of this cell are still up
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def is_fully_closed(self, cell):
        return all(cell.walls.values())

    def close_cell(self, grid, x, y):
        cell = grid[y][x]
        cell.visited = True

<<<<<<< HEAD:cells.py
=======
# Pre-mark the cells that form the digit "4" starting at (x,y)
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def draw_4(self, grid, x, y):
        coords = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
                            (2, 3),
                            (2, 4)
        ]

        for dx, dy in coords:
            self.close_cell(grid, x + dx, y + dy)

<<<<<<< HEAD:cells.py
=======
# Pre-mark the cells that form the digit "2" starting at (x,y)
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def draw_2(self, grid, x, y):
        coords = [
            (0, 0), (1, 0), (2, 0),
                            (2, 1),
            (0, 2), (1, 2), (2, 2),
            (0, 3),
            (0, 4), (1, 4), (2, 4)
        ]

        for dx, dy in coords:
            self.close_cell(grid, x + dx, y + dy)

<<<<<<< HEAD:cells.py
=======
    # Center the "42" shape in the grid and call draw_4 + draw_2
    # Raises ValueError if the maze is too small to fit the pattern
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def place_42_pattern(self, grid):
        height = self.height
        width = self.width

        pattern_width = 7
        pattern_height = 5

        if width < 11 or height < 9:
            raise ValueError("maze too small for 42 pattern")

        start_x = (width - pattern_width) // 2
        start_y = (height - pattern_height) // 2

        self.draw_4(grid, start_x, start_y)
        self.draw_2(grid, start_x + 4, start_y)

        return True

<<<<<<< HEAD:cells.py
=======
    # Convert a cell's wall state to a single hex digit (0–F)
    # Each bit in the result represents one wall: N=1, E=2, S=4, W=8
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def encoded_cell(self, cell):
        value = 0

        for dir, bit in self.wall_bits.items():
            if cell.walls[dir]:
                value |= bit

        return value

<<<<<<< HEAD:cells.py
=======
    # Encode every cell row by row, return as a list of hex strings
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def encoded_grid(self, grid):
        lines = []
        for row in grid:
            line = ""
            for cell in row:
                encoded = self.encoded_cell(cell)
                line += format(encoded, "X")
            lines.append(line)

        return lines

<<<<<<< HEAD:cells.py
=======
    # Write the encoded grid to an open file, one row per line
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def write_maze(self, file, grid):
        lines = self.encoded_grid(grid)
        for line in lines:
            file.write(line + "\n")

<<<<<<< HEAD:cells.py
=======
    # Write entry and exit coordinates to the output file
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def write_entry_exit_(self, file, entry, exit_):
        file.write(f"{entry[0]}, {entry[1]}\n")
        file.write(f"{exit_[0]}, {exit_[1]}\n")

<<<<<<< HEAD:cells.py
=======
    # Write the complete output file:
        # hex grid → blank line → entry → exit → space-separated path
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def write_output(self, grid, path):
        filename = self.output_file
        entry = self.entry
        exit_ = self.exit_
        with open(filename, "w") as file:
            self.write_maze(file, grid)
            file.write("\n")
            self.write_entry_exit_(file, entry, exit_)
            file.write("\n")
            file.write(" ".join(path) + "\n")

<<<<<<< HEAD:cells.py
=======
    # Return True if moving this direction from (x,y) is not blocked by a wall
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def can_move(self, grid, x, y, direction):
        cell = grid[y][x]

        if cell.walls[direction]:
            return False

        return True

<<<<<<< HEAD:cells.py
=======
    # BFS from entry to exit
    # Returns a parent dict: {cell: (previous_cell, direction)}
    # Used by reconstruct_path to trace the route back
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def bfs_algo(self, grid, entry, exit_):
        queue = deque()
        visited = set()
        parent = {}

        queue.append(entry)
        visited.add(entry)

        while queue:
            x, y = queue.popleft()

            if (x, y) == exit_:
                return parent

            for d in self.directions:
                if self.can_move(grid, x, y, d):
                    dx, dy = self.directions[d]
                    nx, ny = x + dx, y + dy

                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = ((x, y), d)
                        queue.append((nx, ny))
        return None

    def reconstruct_path(self, parent, entry, exit_):
        path = []
        current = exit_

        while current != entry:
            prev, direction = parent[current]
            path.append(direction)
            current = prev

        path.reverse()
        return path

<<<<<<< HEAD:cells.py
=======
    # Call bfs_algo then reconstruct_path and return the direction list
    # Returns [] if no path exists
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def shortest_path(self, grid):
        parent = self.bfs_algo(grid, self.entry, self.exit_)

        if parent is None:
            return []
        return self.reconstruct_path(parent, self.entry, self.exit_)

<<<<<<< HEAD:cells.py
=======
    # Convert a direction list into a list of (x,y) coordinate tuples
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def path_to_coords(self, path):
        entry = self.entry
        coords = [entry]
        x, y = entry

        for d in path:
            dx, dy = self.directions[d]
            x += dx
            y += dy
            coords.append((x, y))

        return coords

<<<<<<< HEAD:cells.py
=======
    # Randomly remove ~10% of remaining walls to introduce loops
    # Only runs when PERFECT=False — creates an imperfect maze
    # Skips fully closed cells (42 pattern) to preserve the shape
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def break_random_walls(self, grid, pro=0.1):
        for row in grid:
            for cell in row:

                if self.is_fully_closed(cell):
                    continue

                for direction, (dx, dy) in self.directions.items():
                    nx, ny = cell.x + dx, cell.y + dy

                    if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                        neighbor = grid[ny][nx]

                        if self.is_fully_closed(neighbor):
                            continue
                        if (cell.walls[direction] and random.random() < pro):
                            self.remove_wall(cell, neighbor, direction)

<<<<<<< HEAD:cells.py
=======
    # Seed Python's random module so generation is reproducible
>>>>>>> bc97e48 (42 color change and fixing):MazeGenerator.py
    def init_random(self):
        seed = self.seed
        random.seed(seed)
