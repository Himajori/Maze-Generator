# *This activity has been created as part of the 42 curriculum by `bmanalla` and `jhima`.*

# A-Maze-ing

> A configurable maze generator written in **Python 3** that creates valid random mazes, exports them using a hexadecimal wall representation, computes the shortest path, and provides a visual representation of the generated maze.

---

# Description

**A-Maze-ing** is a maze generation project developed as part of the **42 Curriculum**.

The objective of the project is to design and implement a complete maze generation system capable of:

* Generating random, fully connected mazes
* Supporting reproducible generation through random seeds
* Producing both perfect and non-perfect mazes
* Exporting mazes in a hexadecimal wall encoding format
* Computing the shortest path between the entrance and exit
* Rendering the maze visually
* Providing a reusable Python package for future projects

The project combines concepts from:

* Graph Theory
* Recursive Algorithms
* Randomized Algorithms
* Pathfinding
* Software Engineering
* Object-Oriented Programming

---

# Features

* Random maze generation
* Configurable maze dimensions
* Perfect maze generation (single unique solution)
* Optional random seed for reproducibility
* Automatic shortest path computation
* Hexadecimal wall encoding
* ASCII or graphical maze rendering
* Interactive visualization
* Reusable `MazeGenerator` module
* Error handling for invalid configurations
* Modular architecture

---

#  Technologies

* Python 3.10+
* Object-Oriented Programming
* Type Hints
* Flake8
* MyPy
* Makefile
* Git

---

# Project Structure

```text
#to be continued 
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<username>/A-Maze-ing.git
cd A-Maze-ing
```

Install dependencies:

```bash
make install
```

or

```bash
pip install -r requirements.txt
```

---

# Running the Project

Execute:

```bash
python3 a_maze_ing.py config.txt
```

or

```bash
make run
```

---

# Configuration File

The maze is configured through a text file using the following format:

```text
WIDTH=20
HEIGHT=15

ENTRY=0,0
EXIT=19,14

OUTPUT_FILE=maze.txt

PERFECT=True

SEED=42
```

## Parameters

| Key               | Description                             |
| ----------------- | --------------------------------------- |
| WIDTH             | Maze width                              |
| HEIGHT            | Maze height                             |
| ENTRY             | Entrance coordinates                    |
| EXIT              | Exit coordinates                        |
| OUTPUT_FILE       | Output filename                         |
| PERFECT           | Generate a perfect maze                 |
| SEED *(optional)* | Random seed for reproducible generation |

---

# Maze Generation Algorithm

**Algorithm Used: Recursive Backtracker (iterative Depth-First Search)**

The maze is carved out of a fully-walled grid using an iterative depth-first search with an explicit stack:

1. Start at the top-left cell, mark it visited, and push it onto the stack.
2. While the stack is not empty, look at the cell on top of the stack:
   * If it has any unvisited neighbors, pick one at random, remove the wall between the two cells, mark the neighbor visited, and push it onto the stack.
   * If it has no unvisited neighbors, pop it off the stack (backtrack).
3. The maze is complete once the stack empties and every reachable cell has been visited.

For **non-perfect** mazes, an extra pass randomly removes a small percentage of the remaining walls after generation, introducing loops so more than one path exists between the entrance and exit.

Once the maze is carved, the shortest route between entrance and exit is computed with a **Breadth-First Search (BFS)**, which guarantees the shortest path in an unweighted grid.

Example:

```text
Stack: [(0,0)]
(0,0) has unvisited neighbors E, S -> pick E -> wall removed -> push (1,0)
Stack: [(0,0), (1,0)]
(1,0) has unvisited neighbor S -> pick S -> wall removed -> push (1,1)
Stack: [(0,0), (1,0), (1,1)]
(1,1) has no unvisited neighbors -> pop -> backtrack to (1,0)
...continues until the stack is empty and every cell has been visited.
```

### Why this algorithm?

It was selected because it:

* Generates perfect mazes naturally
* Produces long and interesting corridors
* Is simple to implement
* Has linear time complexity
* Requires minimal memory

---

# Maze Representation

Each maze cell stores four walls:

* North
* East
* South
* West

The walls are encoded using one hexadecimal digit.

Example:

| Binary | Hex | Meaning                   |
| ------ | --- | ------------------------- |
| 0000   | 0   | No walls                  |
| 0011   | 3   | North & East walls closed |
| 1010   | A   | East & West walls closed  |
| 1111   | F   | All walls closed          |

---

# Shortest Path

After generating the maze, the program computes the shortest valid route between the entrance and exit.

The resulting path is stored using movement directions:

```text
N
E
S
W
```

The visual renderer can optionally display this solution.

---

#  Visualization

The maze can be displayed using:

* ASCII rendering in the terminal

After the maze is drawn, an interactive menu is shown:

```text
1) Generate a new maze
2) Show/Hide the shortest path
3) Change wall color
4) Exit
```

* **Generate a new maze** re-runs generation with the same width, height, entry, and exit, producing a fresh random layout.
* **Show/Hide the shortest path** toggles the solution overlay on the existing maze without regenerating it.
* **Change wall color** lets you pick from a list of ANSI colors (red, green, yellow, blue, magenta, cyan, white) for the walls.

---

#  Reusable Module

One objective of the project is code reusability.

The reusable package exposes a `MazeGenerator` class that can be imported into other Python projects.


The module provides access to:

* Generated maze structure
* Entrance
* Exit
* Shortest solution
* Configuration options

---

# Output Format

The generated maze is exported as:

```text
A9C3F...
...

ENTRY=0,0
EXIT=19,14
EESSWWNN...
```

The file contains:

* Maze hexadecimal encoding
* Entry coordinates
* Exit coordinates
* Shortest path

---

#  Makefile Commands

```bash
make install
```

Install dependencies.

```bash
make run
```

Run the application.

```bash
make debug
```

Run in debug mode.

```bash
make lint
```

Run Flake8 and MyPy.

```bash
make clean
```

Remove temporary files and caches.

---

#  Testing

The project has been tested with:

* Small mazes
* Large mazes
* Perfect mazes
* Invalid configuration files
* Edge-case dimensions
* Reproducible seeds

---

## Project Planning

The project followed an iterative development process:

1. Requirements analysis
2. Maze representation
3. Generation algorithm
4. Pathfinding
5. Visualization
6. Testing
7. Documentation

---

## What Worked Well

* Modular architecture
* Separation of responsibilities
* Reusable generator module
* Configuration-driven design

---

## Project Management Tools

* Git
* GitHub
* VS Code / PyCharm
* Python Virtual Environment

---

# Resources

## Documentation

* Python Documentation
* PEP 8 Style Guide
* Flake8
* MyPy Documentation

## Algorithms

* Recursive Backtracker
* Breadth-First Search (BFS)
* Depth-First Search (DFS)

## AI Usage

Artificial Intelligence tools were used to assist with:

* Documentation drafting
* Code review
* Debugging assistance
* Refactoring suggestions
* README structure improvements

All generated content was reviewed, tested, and adapted before inclusion in the final project.

---

