REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")

MIN_WIDTH = 2
MIN_HEIGHT = 2

MAX_WIDTH = 100
MAX_HEIGHT = 100


def read_key_values(path: str) -> dict[str, str]:
    values = {}
    with open(path) as file:
        for line in file:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if "=" not in line:
                raise ValueError(f"invalid config line: {line!r}")
            key, _, value = line.partition("=")
            values[key.strip().upper()] = value.strip()
    return values


def check_required_keys(raw: dict[str, str]) -> None:
    missing = [key for key in REQUIRED_KEYS if key not in raw]
    if missing:
        raise ValueError(
            f"missing required config key(s): "
            f"{', '.join(missing)}")


def parse_int(raw: dict[str, str], key: str) -> int:
    try:
        return int(raw[key])
    except ValueError:
        raise ValueError(f"{key} must be an integer")


def parse_coord(raw: dict[str, str], key: str) -> tuple[int, int]:
    parts = raw[key].split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} must be in the form x,y")
    try:
        return (int(parts[0].strip()), int(parts[1].strip()))
    except ValueError:
        raise ValueError(f"{key} must contain integer coordinates")


def parse_bool(raw: dict[str, str], key: str) -> bool:
    # PERFECT is a required, strictly-typed boolean: only the exact
    # values "True" or "False" are accepted. Anything else (empty,
    # "yes"/"no", "1"/"0", or arbitrary text) is an error — there is
    # no silent fallback to a default.
    value = raw[key].strip()
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"{key} must be either True or False")


def parse_optional_int(raw: dict[str, str], key: str) -> int | None:
    value = raw.get(key, "").strip()
    return int(value) if value else None


def check_in_bounds(
    key: str,
    coord: tuple[int, int],
    width: int,
    height: int,
) -> None:
    x, y = coord
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"{key} {x},{y} falls outside the "
            f"{width}x{height} grid")


def check_dimensions(width: int, height: int) -> None:
    # Validate maze dimensions are large enough to be usable
    if width < MIN_WIDTH:
        raise ValueError(
            f"WIDTH must be at least {MIN_WIDTH}, got {width}")
    if height < MIN_HEIGHT:
        raise ValueError(
            f"HEIGHT must be at least {MIN_HEIGHT}, got {height}")

    # validate maze dimensions if larger than they should
    if width > MAX_WIDTH:
        raise ValueError(
            f"WIDTH cannot exceed {MAX_WIDTH}, got {width}")

    if height > MAX_HEIGHT:
        raise ValueError(
            f"HEIGHT cannot exceed {MAX_HEIGHT}, got {height}")


def check_entry_exit_same(
    entry: tuple[int, int],
    exit_: tuple[int, int]
) -> None:
    # Raise if entry and exit are the same cell
    if entry == exit_:
        raise ValueError(
            f"ENTRY and EXIT must be different cells, "
            f"both are {entry[0]},{entry[1]}")


def get_42_cells(width: int, height: int) -> set[tuple[int, int]]:
    # Return the set of (x,y) cells that will be occupied by the 42 pattern
    # Mirrors the coords in draw_4 and draw_2 exactly
    start_x = (width - 7) // 2
    start_y = (height - 5) // 2

    coords_4 = [
        (0, 0),
        (0, 1),
        (0, 2), (1, 2), (2, 2),
                        (2, 3),
                        (2, 4),
    ]
    coords_2 = [
        (0, 0), (1, 0), (2, 0),
                        (2, 1),
        (0, 2), (1, 2), (2, 2),
        (0, 3),
        (0, 4), (1, 4), (2, 4),
    ]

    cells = set()
    for dx, dy in coords_4:
        cells.add((start_x + dx, start_y + dy))
    for dx, dy in coords_2:
        cells.add((start_x + 4 + dx, start_y + dy))

    return cells


def check_entry_exit_not_on_42(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> None:
    # Entry and exit must not land on a fully-closed 42 pattern cell.
    # Only applies when the maze is large enough to place the pattern.
    if width < 11 or height < 9:
        return

    cells_42 = get_42_cells(width, height)

    if entry in cells_42:
        raise ValueError(
            f"ENTRY {entry[0]},{entry[1]} overlaps with the 42 pattern — "
            f"choose a different entry coordinate")
    if exit_ in cells_42:
        raise ValueError(
            f"EXIT {exit_[0]},{exit_[1]} overlaps with the 42 pattern — "
            f"choose a different exit coordinate")


def parse_config(
    path: str,
) -> dict[str, int | bool | str | tuple[int, int] | None]:
    raw = read_key_values(path)
    check_required_keys(raw)

    width = parse_int(raw, "WIDTH")
    height = parse_int(raw, "HEIGHT")

    # Validate dimensions before anything else
    check_dimensions(width, height)

    entry = parse_coord(raw, "ENTRY")
    exit_ = parse_coord(raw, "EXIT")

    check_in_bounds("ENTRY", entry, width, height)
    check_in_bounds("EXIT", exit_, width, height)
    check_entry_exit_same(entry, exit_)
    check_entry_exit_not_on_42(width, height, entry, exit_)

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit_": exit_,
        "seed": parse_optional_int(raw, "SEED"),
        "perfect": parse_bool(raw, "PERFECT"),
        "output_file": raw["OUTPUT_FILE"],

    }
