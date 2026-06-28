import cells as maze_module


GREEN   = "\033[92m"
RED     = "\033[91m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
RESET   = "\033[0m"


def render_in_ascii(grid, path_coords, entry, exit_,
                    color_42=RESET, color_wall=YELLOW):

    height = len(grid)
    width = len(grid[0])

    print(f"{color_wall}╔{RESET}" + f"{color_wall}═══╦{RESET}" * (width - 1) + f"{color_wall}═══╗{RESET}")

    for y in range(height):
        line_cells = f"{color_wall}║{RESET}"
        line_walls = f"{color_wall}╠{RESET}"

        for x in range(width):
            cell = grid[y][x]

            if (x, y) == entry:
                content = f"{YELLOW} ♛ {RESET}"
            elif (x, y) == exit_:
                content = f"{YELLOW} ⚑ {RESET}"
            elif maze.is_fully_closed(cell):
                content = f"{color_42}███{RESET}"
            elif (x, y) in path_coords:
                content = f"{GREEN} ⬢ {RESET}"
            else:
                content = "   "

            line_cells += content
            line_cells += f"{color_wall}║{RESET}" if cell.walls["E"] else " "

            line_walls += f"{color_wall}═══{RESET}" if cell.walls["S"] else "   "
            line_walls += f"{color_wall}╬{RESET}" if x < width - 1 else f"{color_wall}╣{RESET}"

        print(line_cells)

        if y != height - 1:
            print(line_walls)

    print(f"{color_wall}╚{RESET}" + f"{color_wall}═══╩{RESET}" * (width - 1) + f"{color_wall}═══╝{RESET}")



def create_maze(width, height, entry, exit_, seed, perfect, output_file):

    maze = maze_module.MazeGenerator(
        width,
        height,
        entry,
        exit_,
        perfect,
        output_file,
        seed
    )

    grid = maze.create_grid()

    if width >= 11 and height >= 9:
        maze.place_42_pattern(grid)

    if seed is not None:
        maze.init_random()

    maze.generate_maze(grid)

    if not perfect:
        maze.break_random_walls(grid)

    path = maze.shortest_path(grid)
    path_coords = maze.path_to_coords(path)

    maze.write_output(grid, path)

    if maze.has_3x3_open(grid):
        raise ValueError("Maze has open area")

    return maze, grid, path_coords

maze, grid, coords = create_maze(
    width=11,
    height=9,
    entry=(10, 8),
    exit_=(0, 0),
    seed=42,
    perfect=True,
    output_file="test.txt"
)
print(coords)
render_in_ascii(
    grid,
    coords,
    (10, 8),
    (0, 0),
    BLUE,
    RED
)