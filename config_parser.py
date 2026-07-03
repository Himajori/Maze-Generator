REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE")


def read_key_values(path):
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


def check_required_keys(raw):
    missing = [key for key in REQUIRED_KEYS if key not in raw]
    if missing:
        raise ValueError(
            f"missing required config key(s): "
            f"{', '.join(missing)}")


def parse_int(raw, key):
    try:
        return int(raw[key])
    except ValueError:
        raise ValueError(f"{key} must be an integer")


def parse_coord(raw, key):
    parts = raw[key].split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} must be in the form x,y")
    try:
        return (int(parts[0].strip()), int(parts[1].strip()))
    except ValueError:
        raise ValueError(f"{key} must contain integer coordinates")


def parse_bool(raw, key, default):
    return raw.get(key, str(default)).strip().lower() == "true"


def parse_optional_int(raw, key):
    value = raw.get(key, "").strip()
    return int(value) if value else None


def check_in_bounds(key, coord, width, height):
    x, y = coord
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"{key} {x},{y} falls outside the "
            f"{width}x{height} grid")


def parse_config(path):
    raw = read_key_values(path)
    check_required_keys(raw)

    width = parse_int(raw, "WIDTH")
    height = parse_int(raw, "HEIGHT")
    entry = parse_coord(raw, "ENTRY")
    exit_ = parse_coord(raw, "EXIT")

    check_in_bounds("ENTRY", entry, width, height)
    check_in_bounds("EXIT", exit_, width, height)

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit_": exit_,
        "seed": parse_optional_int(raw, "SEED"),
        "perfect": parse_bool(raw, "PERFECT", default=True),
        "output_file": raw["OUTPUT_FILE"],
    }
