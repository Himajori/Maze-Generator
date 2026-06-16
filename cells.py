class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            "up": True,
            "right": True,
            "down": True,
            "left": True
        }


def create_grid(width: int, height:int):
    grid = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(Cell(x, y))
        grid.append(row)
    return grid


grid = create_grid(3,3)
for row in grid:
    print([f"({c.x}, {c.y})" for c in row])