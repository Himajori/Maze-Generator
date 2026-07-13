from typing import Any, Callable


def clear_screen() -> None:
    print("\033c", end="")


def prompt(message: str) -> str:
    try:
        return input(message).strip()
    except (EOFError, KeyboardInterrupt):
        return "4"


def choose_color(colors: dict[str, tuple[str, str]]) -> str | None:
    print("\nAvailable colors:")
    for key, (name, _) in colors.items():
        print(f"  {key}) {name}")

    choice = prompt("Pick a color: ")
    if choice not in colors:
        print("Invalid choice, keeping current color.")
        return None
    return colors[choice][1]


def regenerate(config: dict[str, Any], create_maze: Callable[..., Any]) -> Any:
    fresh_config = dict(config)
    fresh_config["seed"] = 42
    return create_maze(**fresh_config)


def run_menu(
            config: dict[str, Any],
            create_maze: Callable[..., Any],
            render_in_ascii: Callable[..., None],
            wall_colors: dict[str, tuple[str, str]],
            wall_color: str,
            color_42: str,) -> None:
    ...
    maze, grid, path_coords = create_maze(**config)
    show_path = True

    while True:
        clear_screen()
        render_in_ascii(
            grid,
            path_coords if show_path else [],
            config["entry"],
            config["exit_"],
            maze,
            color_42,
            wall_color,
        )

        print("\n1) Generate a new maze")
        print(f"2) {'Hide' if show_path else 'Show'} the shortest path")
        print("3) Change wall color")
        print("4) Change 42 wall color")
        print("5) Exit")

        choice = prompt("> ")

        if choice == "1":
            maze, grid, path_coords = regenerate(config, create_maze)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            new_color = choose_color(wall_colors)
            if new_color is not None:
                wall_color = new_color
        elif choice == "4":
            new_color = choose_color(wall_colors)
            if new_color is not None:
                color_42 = new_color
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
