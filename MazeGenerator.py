import random
from collections import deque
from typing import IO, TypeAlias


class MazeGenerator():
    ParentMap: TypeAlias = dict[
        tuple[int, int],
        tuple[tuple[int, int], str],
    ]

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool,
        output_file: str,
        seed: int | None = None
    ) -> None:
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
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y
            self.visited = False
            self.walls: dict[str, bool] = {
                "N": True,
                "E": True,
                "S": True,
                "W": True
            }
    # Build a 2D list (height x width) of Cell objects, all walls up

    def create_grid(self) -> list[list[Cell]]:
        grid = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(MazeGenerator.Cell(x, y))
            grid.append(row)

        return grid

    # Return existing adjacent cells as {direction: cell}
    # Only includes directions that are inside the grid bounds
    def get_neighbors(
        self,
        cell: Cell,
        grid: list[list[Cell]]
    ) -> dict[str, Cell]:
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

    # Remove the wall between two adjacent cells on both sides
    def remove_wall(self, cell: Cell, neighbor: Cell, direction: str) -> None:
        cell.walls[direction] = False
        neighbor.walls[self.opposite[direction]] = False

    # Filter get_neighbors() to only cells not yet visited by DFS
    def get_unvisted_neighbors(
        self,
        cell: Cell,
        grid: list[list[Cell]]
    ) -> dict[str, Cell]:
        neighbors = self.get_neighbors(cell, grid)

        unvisted_neighbors = {}
        for dir in neighbors:
            neighbor = neighbors[dir]
            if not neighbor.visited:
                unvisted_neighbors[dir] = neighbor

        return unvisted_neighbors

    # Run iterative DFS from grid[0][0] using an explicit stack
        # Keeps carving until every reachable cell has been visited
        # Cells pre-marked visited (42 pattern) are skipped automatically
    def dfs_algo(self, cell: Cell, grid: list[list[Cell]]) -> Cell | None:
        unvisited = self.get_unvisted_neighbors(cell, grid)

        if not unvisited:
            return None

        direction = random.choice(list(unvisited.keys()))
        neighbor = unvisited[direction]

        self.remove_wall(cell, neighbor, direction)
        neighbor.visited = True

        return neighbor

    def generate_maze(self, grid: list[list[Cell]]) -> None:
        # Run iterative DFS from grid[0][0] using an explicit stack
        # Keeps carving until every reachable cell has been visited

        self.init_random()
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

    # Return True if every cell in the grid has been visit
    def all_cells_visited(self, grid: list[list[Cell]]) -> bool:
        for row in grid:
            for cell in row:
                if not cell.visited:
                    return False
        return True

    # Scan the whole grid for any 3x3 block that is fully open
    # The maze constraint forbids corridors wider than 2 cells
    def has_3x3_open(self, grid: list[list[Cell]]) -> bool:
        height = self.height
        width = self.width

        for y in range(height - 2):
            for x in range(width - 2):
                if self.is_3x3_open(grid, x, y):
                    return True
        return False

    # Check if the specific 3x3 block starting at (x,y) has no
    # internal East or South walls (fully open area)
    def is_3x3_open(self, grid: list[list[Cell]], x: int, y: int) -> bool:
        for dy in range(3):
            for dx in range(3):
                cell = grid[dy + y][dx + x]

                if dx < 2 and cell.walls["E"]:
                    return False
                if dy < 2 and cell.walls["N"]:
                    return False
        return True

    # Return True if all 4 walls of this cell are still up
    def is_fully_closed(self, cell: Cell) -> bool:
        return all(cell.walls.values())

    def close_cell(self, grid: list[list[Cell]], x: int, y: int) -> None:
        cell = grid[y][x]
        cell.visited = True

# Pre-mark the cells that form the digit "4" starting at (x,y)
    def draw_4(self, grid: list[list[Cell]], x: int, y: int) -> None:
        coords = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
                            (2, 3),
                            (2, 4)
        ]

        for dx, dy in coords:
            self.close_cell(grid, x + dx, y + dy)

# Pre-mark the cells that form the digit "2" starting at (x,y)
    def draw_2(self, grid: list[list[Cell]], x: int, y: int) -> None:
        coords: list[tuple[int, int]] = [
            (0, 0), (1, 0), (2, 0),
                            (2, 1),
            (0, 2), (1, 2), (2, 2),
            (0, 3),
            (0, 4), (1, 4), (2, 4)
        ]

        for dx, dy in coords:
            self.close_cell(grid, x + dx, y + dy)

    # Center the "42" shape in the grid and call draw_4 + draw_2
    # Raises ValueError if the maze is too small to fit the pattern
    def place_42_pattern(self, grid: list[list[Cell]]) -> bool:
        height = self.height
        width = self.width

        pattern_width = 7
        pattern_height = 5

        if width < 11 or height < 9:
            raise ValueError("maze too small for 42 pattern")

        start_x = (width - pattern_width) // 2
        start_y = (height - pattern_height) // 2

        # On even widths, dead-centering the pattern lands the grid's exact
        # centre cell on a sealed "2" cell, so a non-perfect maze can never
        # open its centre (a Pac-Man-usability requirement). Column 3 of the
        # pattern is always an empty gap, so nudging one cell right moves the
        # centre column there instead, regardless of height's parity.
        if width % 2 == 0:
            start_x += 1

        self.draw_4(grid, start_x, start_y)
        self.draw_2(grid, start_x + 4, start_y)

        return True

    # Convert a cell's wall state to a single hex digit (0–F)
    # Each bit in the result represents one wall: N=1, E=2, S=4, W=8
    def encoded_cell(self, cell: Cell) -> int:
        value = 0

        for dir, bit in self.wall_bits.items():
            if cell.walls[dir]:
                value |= bit

        return value

    # Encode every cell row by row, return as a list of hex strings
    def encoded_grid(self, grid: list[list[Cell]]) -> list[str]:
        lines = []
        for row in grid:
            line = ""
            for cell in row:
                encoded = self.encoded_cell(cell)
                line += format(encoded, "X")
            lines.append(line)

        return lines

    # Write the encoded grid to an open file, one row per line
    def write_maze(self, file: IO[str], grid: list[list[Cell]]) -> None:
        lines = self.encoded_grid(grid)
        for line in lines:
            file.write(line + "\n")

    # Write entry and exit coordinates to the output file
    def write_entry_exit_(
        self,
        file: IO[str],
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> None:
        file.write(f"{entry[0]}, {entry[1]}\n")
        file.write(f"{exit_[0]}, {exit_[1]}\n")

    # Write the complete output file:
        # hex grid → blank line → entry → exit → space-separated path
    def write_output(self, grid: list[list[Cell]], path: list[str]) -> None:
        filename = self.output_file
        entry = self.entry
        exit_ = self.exit_
        with open(filename, "w") as file:
            self.write_maze(file, grid)
            file.write("\n")
            self.write_entry_exit_(file, entry, exit_)
            file.write("\n")
            file.write(" ".join(path) + "\n")

    # Return True if moving this direction from (x,y) is not blocked by a wall
    def can_move(
        self,
        grid: list[list[Cell]],
        x: int,
        y: int,
        direction: str
    ) -> bool:
        cell = grid[y][x]

        if cell.walls[direction]:
            return False

        return True

    # BFS from entry to exit
    # Returns a parent dict: {cell: (previous_cell, direction)}
    # Used by reconstruct_path to trace the route back
    def bfs_algo(
        self,
        grid: list[list[Cell]],
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> ParentMap | None:
        queue: deque[tuple[int, int]] = deque()
        visited: set[tuple[int, int]] = set()
        parent: dict[
            tuple[int, int],
            tuple[tuple[int, int], str],
        ] = {}

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

    def reconstruct_path(
        self,
        parent: ParentMap,
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> list[str]:
        path = []
        current = exit_

        while current != entry:
            prev, direction = parent[current]
            path.append(direction)
            current = prev

        path.reverse()
        return path

    # Call bfs_algo then reconstruct_path and return the direction list
    # Returns [] if no path exists
    def shortest_path(self, grid: list[list[Cell]]) -> list[str]:
        parent = self.bfs_algo(grid, self.entry, self.exit_)

        if parent is None:
            return []
        return self.reconstruct_path(parent, self.entry, self.exit_)

    # Convert a direction list into a list of (x,y) coordinate tuples
    def path_to_coords(self, path: list[str]) -> list[tuple[int, int]]:
        entry = self.entry
        coords = [entry]
        x, y = entry

        for d in path:
            dx, dy = self.directions[d]
            x += dx
            y += dy
            coords.append((x, y))

        return coords

    # Randomly remove ~10% of remaining walls to introduce loops
    # Only runs when PERFECT=False — creates an imperfect maze
    # Skips fully closed cells (42 pattern) to preserve the shape
    def break_random_walls(
        self,
        grid: list[list[Cell]],
        pro: float = 0.1
    ) -> None:
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

    # Return how many walls on this cell are open (0–4)
    def count_open_walls(self, cell: Cell) -> int:
        return sum(1 for w in cell.walls.values() if not w)

    # A dead-end has exactly 1 open passage and 3 walls still up
    def is_dead_end(self, cell: Cell) -> bool:
        return self.count_open_walls(cell) == 1

    # Collect every non-42-pattern dead-end cell in the grid
    def get_dead_ends(self, grid: list[list[Cell]]) -> list[Cell]:
        dead_ends = []
        for row in grid:
            for cell in row:
                if self.is_fully_closed(cell):
                    continue  # skip 42 pattern cells
                if self.is_dead_end(cell):
                    dead_ends.append(cell)
        return dead_ends

    # Temporarily open a wall, check for 3x3 open area, then restore
    def would_create_3x3_open(
        self,
        grid: list[list[Cell]],
        cell: Cell,
        neighbor: Cell,
        direction: str
    ) -> bool:
        self.remove_wall(cell, neighbor, direction)
        result = self.has_3x3_open(grid)
        cell.walls[direction] = True
        neighbor.walls[self.opposite[direction]] = True
        return result

    # Open walls on dead-end cells until at most max_dead_ends remain.
    # Skips 42-pattern cells and walls that would create a 3x3 open area.
    def reduce_dead_ends(
        self,
        grid: list[list[Cell]],
        max_dead_ends: int = 2
    ) -> None:
        for _ in range(len(grid) * len(grid[0])):  # safety cap
            dead_ends = self.get_dead_ends(grid)
            if len(dead_ends) <= max_dead_ends:
                break

            random.shuffle(dead_ends)

            progress = False
            for cell in dead_ends:
                neighbors = self.get_neighbors(cell, grid)
                dirs = list(neighbors.keys())
                random.shuffle(dirs)

                for direction in dirs:
                    neighbor = neighbors[direction]
                    # never open into a 42-pattern cell
                    if self.is_fully_closed(neighbor):
                        continue
                    # wall already open — nothing to do
                    if not cell.walls[direction]:
                        continue
                    # skip if it would create a forbidden 3x3 open area
                    if self.would_create_3x3_open(
                            grid, cell, neighbor, direction
                    ):
                        continue
                    self.remove_wall(cell, neighbor, direction)
                    progress = True
                    break

            # If nothing could be opened this pass, stop to avoid infinite loop
            if not progress:
                break

    # Seed Python's random module so generation is reproducible
    def init_random(self) -> None:
        seed = self.seed
        random.seed(seed)
