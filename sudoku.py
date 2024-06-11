import random
import sys
import pygame
import threading


# Constants

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

input_action = None  # Global variable to track input actions


# Utility function 1: find_mrv_cell()
def find_mrv_cell(grid):
    # min_count could be set to 9 instead of float('inf'). However, initializing it to float('inf') is a more generic and conventional way of indicating an initially very high value that any real count of legal values will be less than.
    min_count = float(
        "inf"
    )  # Initialized to infinity. This variable will keep track of the minimum number of legal values found for any cell.
    min_cell = None  # Initialized to None. This variable will store the coordinates of the cell with the fewest legal values.
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                valid_values = get_valid_values(grid, r, c)
                # If the number of legal values for the current cell is less than min_count, the function updates min_count to this new lower number.
                if len(valid_values) < min_count:
                    min_count = len(valid_values)
                    min_cell = (
                        r,
                        c,
                    )  # Updates min_cell to the coordinates of the current cell.
    # After iterating through all cells, the function returns the coordinates of the cell with the fewest valid values.
    return min_cell


# Utility function 2: get_valid_values(grid, row, col); grid is the current state of the Sudoku grid
def get_valid_values(grid, row, col):
    valid_values = set(range(1, GRID_SIZE + 1))  # Set valid_values to a set of 1 to 10

    # grid[row] returns the entire row as a list. set(grid[row]) converts this list to a set of values present in that row. valid_values -= set(grid[row]) subtracts these values from the initial set of valid values.
    valid_values -= set(
        grid[row]
    )  # Remove the values already present in the same row from the set of valid values.

    # Remove the values already present in the same column from the set of valid values.
    # Loop through each row index r in the grid. For each row, grid[r][col] accesses the value in the specified column. valid_values.discard(grid[r][col]) removes this value from the set of valid values if it is present.
    for r in range(GRID_SIZE):
        valid_values.discard(grid[r][col])

    # Calculate the starting indices of the 3x3 subgrid that contains the cell (row, col).
    # (row // 3) and (col // 3) determine the subgrid row and column indices. Multiplying by 3 gives the starting row and column indices of the subgrid.
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    #  Loop through each cell in the 3x3 subgrid starting at (row_start, col_start). For each cell (r, c), grid[r][c] accesses the value in the subgrid. valid_values.discard(grid[r][c]) removes this value from the set of valid values if it is present.
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            valid_values.discard(grid[r][c])

    # After removing values from the row, column, and subgrid, the remaining values in valid_values are the valid candidates for the cell (row, col).
    return valid_values


# Utility function 3: solver(grid)
# Call find_mrv_cell(grid). It returns the cell with the least number of valid values.
def solver(grid):
    empty_cell_pos = find_mrv_cell(grid)

    # If empty_cell_pos is None, return True
    if empty_cell_pos is None:
        return True
    # row, col = empty_cell_pos
    row, col = empty_cell_pos

    # Call get_valid_values()
    valid_values = get_valid_values(grid, row, col)

    # for num in valid_values, assign num to grid[row][col].
    for num in valid_values:
        grid[row][col] = num

        if solver(grid):  # Recursively attempt to solve the grid
            return True

    # If no solution is found, it backtracks and tries the next value.
    return False


# Utility function 4: generate_solved_grid()
def generate_solved_grid():
    # Creates a list of lists representing a 9x9 grid, with all cells initialized to 0; empty grid
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    solver(grid)  # Solving it using the solver function.
    return grid


# Utility function 5: shuffle_grid()
def shuffle_grid(grid):
    # Shuffle numbers within rows and columns
    for row in grid:
        random.shuffle(row)

    # # Loop through each column index
    for col in range(GRID_SIZE):
        # Initialize an empty list to store the numbers in the current column
        nums_in_col = []

        # Loop through each row index to collect the numbers in the current column
        for row in range(GRID_SIZE):
            nums_in_col.append(grid[row][col])

        # Shuffle the collected numbers in the current column
        random.shuffle(nums_in_col)

        # Loop through each row index again to place the shuffled numbers back into the column
        for row in range(GRID_SIZE):
            grid[row][col] = nums_in_col[row]


# Utility function 6: generate_puzzle()
def generate_puzzle(grid, difficulty):
    num_to_remove = 0
    # Initialize cells_to_remove based on the game difficulty levels. For "easy", remove 30 cells; for "medium", remove 45 cells; for "hard", remove 60 cells.
    if difficulty == "easy":
        num_to_remove = 30
    elif difficulty == "medium":
        num_to_remove = 45
    elif difficulty == "hard":
        num_to_remove = 60
    # Call generate_solved_grid(). It returns a fully solved grid.
    solved_grid = generate_solved_grid()
    # grid[:] = solved_grid ensures that the provided grid is overwritten with the solved grid.
    grid[:] = solved_grid
    # shuffle_grid(grid) rearranges the numbers within the grid's rows and columns.
    shuffle_grid(grid)
    # Ensure that the shuffled grid is still a valid and solvable Sudoku puzzle.
    # Copy the grid to temp_grid and check if it is solvable using solver(temp_grid)
    temp_grid = [row[:] for row in grid]
    while not solver(temp_grid):
        shuffle_grid(grid)
        temp_grid = [row[:] for row in grid]

    # Generate a list of tuples representing all cell positions (r, c) in the grid and shuffle this list to randomize the order of cell removal.
    cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(cells)

    # Remove numbers from the grid while ensuring it remains solvable.
    # Loop through the shuffled list of cell positions.
    for r, c in cells:
        temp = grid[r][c]
        # Temporarily remove the number at (r, c) by setting grid[r][c] to 0.
        grid[r][c] = 0
        # Copy the grid to temp_grid and check if it is still solvable using solver(temp_grid).
        temp_grid = [row[:] for row in grid]
        # If the grid is unsolvable without the number, restore the number by setting grid[r][c] back to temp.
        if not solver(temp_grid):
            grid[r][c] = temp
        # If the grid is still solvable, decrement the num_to_remove counter.
        else:
            num_to_remove -= 1
            # Break the loop once the desired number of cells have been removed.
            if num_to_remove == 0:
                break


# Utility function 7: draw_grid()
def draw_grid(screen, grid):
    # screen.fill(BLUE): This line fills the entire screen with the color blue. It acts as a background for the Sudoku grid.
    screen.fill(BLUE)
    # This nested loop iterates over each cell in the grid. r is the row index and c is the column index.
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            # Set value to the cell at position (r, c).
            value = grid[r][c]

            # Checks if the cell is not empty (i.e., the cell contains a number other than 0).
            if value != 0:
                # pygame.draw.rect(...): This function draws a white rectangle on the screen at the position (c * CELL_SIZE, r * CELL_SIZE) with size CELL_SIZE x CELL_SIZE. This rectangle represents the cell.
                pygame.draw.rect(
                    screen, WHITE, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

                # Creates a font object with a size of 40. The None argument means the default font is used.
                font = pygame.font.Font(None, 40)

                # Renders the number value as a text surface with black color.
                text = font.render(str(value), True, BLACK)

                # Creates a rectangle object for the text surface and centers it within the cell. The center position is calculated as (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
                text_rect = text.get_rect(
                    center=(
                        c * CELL_SIZE + CELL_SIZE // 2,
                        r * CELL_SIZE + CELL_SIZE // 2,
                    )
                )

                # Draws the text surface onto the screen at the position defined by text_rect.
                screen.blit(text, text_rect)
    # Updates the entire screen display, making all the changes visible.
    pygame.display.flip()


# Utility function 8: handle_user_input()
def handle_user_input():
    global input_action
    while True:
        action = (
            input(
                "Type 'solve' to solve the current puzzle, 'new' to generate a new puzzle and 'exit' to quit: "
            )
            .strip()
            .lower()
        )
        if action in ["solve", "new", "exit"]:
            input_action = action
            break
        else:
            print("Invalid input. Please enter solve, new or exit.")


# Main function
def main():
    # Declare an input_action global variable to track the user input
    global input_action
    # Initialize all imported Pygame modules
    pygame.init()

    # Create game window and set caption to it
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Game")

    # Set a while loop that runs indefinitely until the game is quit
    while True:
        # Generate a fully solved Sudoku grid using generate_solved_grid()
        solved_grid = generate_solved_grid()

        # Create a copy of the solved grid to modify for the puzzle
        generated_grid = [row[:] for row in solved_grid]
        # Generate puzzle
        generate_puzzle(generated_grid, "medium")

        # Draw the generated puzzle on the screen
        draw_grid(screen, generated_grid)

        # Set input_action to None to prepare for user input. This ensures that the game can continue running and responding to events while waiting for the user to type a command.
        input_action = None
        # Create a new thread to handle user input without blocking the main game loop.
        input_thread = threading.Thread(target=handle_user_input)

        # Start the input handling thread
        input_thread.start()
        # Create an inner while loop that waits for the user to provide an action, where the input_action is set to None.
        while input_action is None:
            # A for loop that iterates over all events in Pygame's event queue.
            for event in pygame.event.get():
                # Checks if the user has requested to quit the game (e.g., by clicking the window's close button).
                if event.type == pygame.QUIT:
                    # Uninitializes all Pygame modules, effectively closing the game window.
                    pygame.quit()
                    # Exits the program.
                    sys.exit()

            # This line limits the loop to run at a maximum of 30 iterations per second (30 FPS). This is important to prevent the loop from consuming too much CPU while waiting for user input.
            pygame.time.Clock().tick(30)

        # If the input_action is "solve",
        if input_action == "solve":
            # Solve the current puzzle, solver()
            solver(generated_grid)
            # Draw the solved puzzle on the screen, draw_grid()
            draw_grid(screen, generated_grid)
            # Set input_action to None, starting a new input handling thread waiting for further input and while loop when input_action is None
            input_action = None
            input_thread = threading.Thread(target=handle_user_input)
            input_thread.start()
            while input_action is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.time.Clock().tick(30)

        # If input_action is "new", use continue to restart the main loop to generate a new puzzle
        elif input_action == "new":
            continue

        # If input_action is "exit", the game exits
        elif input_action == "exit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
