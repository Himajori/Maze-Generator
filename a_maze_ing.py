import sys

<<<<<<< HEAD
import cells as maze_module
=======
import MazeGenerator as maze_module
>>>>>>> bc97e48 (42 color change and fixing)
from config_parser import parse_config
from menu import run_menu


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
NAVY = "\033[38;2;0;0;128m"
MAROON = "\033[38;2;128;0;0m"
RESET = "\033[0m"


def render_in_ascii(grid, path_coords, entry, exit_, maze,
                    color_42=RESET, color_wall=YELLOW):

    height = len(grid)
    width = len(grid[0])

    print(
        f"{color_wall}╔{RESET}"
        + f"{color_wall}═══╦{RESET}" * (width - 1)
        + f"{color_wall}═══╗{RESET}"
    )
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

            line_walls += (
                f"{color_wall}═══{RESET}"
                if cell.walls["S"]
                else "   "
            )

            line_walls += (
                f"{color_wall}╬{RESET}"
                if x < width - 1
                else f"{color_wall}╣{RESET}"
            )
        print(line_cells)

        if y != height - 1:
            print(line_walls)

    print(
        f"{color_wall}╚{RESET}"
        + f"{color_wall}═══╩{RESET}" * (width - 1)
        + f"{color_wall}═══╝{RESET}"
    )


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


WALL_COLORS = {
    "1": ("Red", RED),
    "2": ("Green", GREEN),
    "3": ("Yellow", YELLOW),
    "4": ("Blue", BLUE),
    "5": ("Magenta", MAGENTA),
    "6": ("Cyan", CYAN),
    "7": ("White", WHITE),
    "8": ("Navy", NAVY),
    "9": ("Maroon", MAROON)
}


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    config = parse_config(config_path)

    run_menu(config, create_maze, render_in_ascii, WALL_COLORS, RED, GREEN)
