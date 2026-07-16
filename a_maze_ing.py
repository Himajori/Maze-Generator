import sys
import os
from typing import TypeAlias

import MazeGenerator as maze_module
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

MazeResult: TypeAlias = tuple[
    maze_module.MazeGenerator,
    list[list[maze_module.MazeGenerator.Cell]],
    list[tuple[int, int]],
]


def check_terminal_size(maze_width: int, maze_height: int) -> bool:
    # Each cell is 3 chars wide + 1 border = 4; plus 1 for the leftmost border
    needed_cols = maze_width * 4 + 1
    # Each cell row has a separator row below it, plus top and bottom borders
    needed_rows = maze_height * 2 + 1

    try:
        term = os.get_terminal_size()
        if needed_cols > term.columns or needed_rows > term.lines:
            print(
                f"\033[91mWarning: maze needs {needed_cols}×{needed_rows} "
                f"characters but terminal is {term.columns}×{term.lines}.\n"
                f"Resize your terminal or reduce WIDTH/HEIGHT in config.txt"
                f"\033[0m"
            )
            return False
    except OSError:
        # Can't determine terminal size (e.g. piped output) — skip the check
        pass
    return True


def render_in_ascii(
    grid: list[list[maze_module.MazeGenerator.Cell]],
    path_coords: list[tuple[int, int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    maze: maze_module.MazeGenerator,
    color_42: str = RESET,
    color_wall: str = YELLOW,
) -> None:

    height = len(grid)
    width = len(grid[0])

    check_terminal_size(width, height)
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


def create_maze(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    seed: int | None,
    perfect: bool,
    output_file: str,
) -> MazeResult:
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
        maze.reduce_dead_ends(grid, max_dead_ends=2)

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
    try:
        config = parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: config file '{config_path}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        run_menu(config, create_maze, render_in_ascii, WALL_COLORS, RED, GREEN)
    except ValueError as e:
        print(f"Error during maze generation: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit(0)
