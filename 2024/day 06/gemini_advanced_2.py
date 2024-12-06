# Conversation with Gemini: https://g.co/gemini/share/a1bc67fb74db

def is_guard_path_loop(grid, guard_pos, guard_dir):
    """
    Simulates the guard's path and determines if it's a loop or exits the grid.

    Args:
      grid (list of lists): The lab map.
      guard_pos (tuple): The guard's starting position (row, col).
      guard_dir (str): The guard's starting direction ('U', 'R', 'D', 'L').

    Returns:
      bool: True if the path is a loop, False if the guard exits the grid.
    """
    visited = set()
    visited.add((guard_pos, guard_dir))

    while True:
        row, col = guard_pos
        # Determine the next position based on the current direction
        if guard_dir == 'U':
            next_pos = (row - 1, col)
        elif guard_dir == 'R':
            next_pos = (row, col + 1)
        elif guard_dir == 'D':
            next_pos = (row + 1, col)
        else:  # guard_dir == 'L'
            next_pos = (row, col - 1)

        # Check if the next position is within bounds
        if 0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0]):
            # Check if the next position is an obstacle
            if grid[next_pos[0]][next_pos[1]] == '#':
                # Turn right
                if guard_dir == 'U':
                    guard_dir = 'R'
                elif guard_dir == 'R':
                    guard_dir = 'D'
                elif guard_dir == 'D':
                    guard_dir = 'L'
                else:  # guard_dir == 'L'
                    guard_dir = 'U'
            else:  # Not an obstacle
                guard_pos = next_pos
                # If the guard revisits a position with the same direction, it's a loop
                if (guard_pos, guard_dir) in visited:
                    return True
                visited.add((guard_pos, guard_dir))
        else:  # Out of bounds
            return False


def find_obstruction_positions(filename="input_1.txt"):
    """
    Finds the possible positions for an obstruction to create a loop.

    Args:
      filename (str): The name of the file containing the lab map.

    Returns:
      int: The number of possible obstruction positions.
    """
    with open(filename, 'r') as f:
        grid = [list(line.strip()) for line in f]

    # Find the guard's starting position and direction
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '^':
                guard_pos = (i, j)
                guard_dir = 'U'
            elif grid[i][j] == '>':
                guard_pos = (i, j)
                guard_dir = 'R'
            elif grid[i][j] == 'v':
                guard_pos = (i, j)
                guard_dir = 'D'
            elif grid[i][j] == '<':
                guard_pos = (i, j)
                guard_dir = 'L'

    possible_positions = 0
    # Try placing an obstruction at each empty position
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '.' and (i, j) != guard_pos:
                grid[i][j] = '#'  # Place obstruction
                # Check if the path becomes a loop after placing the obstruction
                if is_guard_path_loop(grid, guard_pos, guard_dir):
                    possible_positions += 1
                grid[i][j] = '.'  # Remove obstruction

    return possible_positions

if __name__ == "__main__":
    result = find_obstruction_positions()
    print(result)
