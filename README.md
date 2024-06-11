# Sudoku Solver and Game with Pygame and MRV Heuristic

This project is a Sudoku solver and game implemented using Python and Pygame. It also incorporates the Minimum Remaining Values (MRV) heuristic to improve the efficiency of the solver.

## Features

- Generate a new Sudoku puzzle
- Solve the current puzzle
- Graphical interface using Pygame
- Implements the MRV heuristic for efficient solving

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-new-sudoku-repo.git
    cd your-new-sudoku-repo
    ```

2. Install the required Python packages:
    ```sh
    pip install pygame
    ```

## Usage

Run the main script to start the game:

```sh
python sudoku.py


## How it works

Generating the Puzzle: The generate_puzzle() function generates a fully solved Sudoku grid, shuffles it to ensure randomness, and then removes numbers while ensuring the puzzle remains solvable.
Solving the Puzzle: The solver uses a backtracking algorithm enhanced with the MRV heuristic to find solutions efficiently.
Graphical Interface: Pygame is used to create a graphical interface where users can see the puzzle and interact with it by typing commands in the console.