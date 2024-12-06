# Conversation with Gemini Advanced: https://g.co/gemini/share/55dca7fd1429

def get_guard_path(filename="input_1.txt"):
    """
    Calculates the number of distinct positions a guard visits in a lab
    and prints the coordinates of the guard when hitting an obstacle or exiting the map.

    Args:
      filename (str): The name of the file containing the lab map.

    Returns:
      int: The number of distinct positions visited by the guard.
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

    visited = set()
    visited.add(guard_pos)

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
                # Print the coordinates before turning right
                print(f"Hit obstacle at: {guard_pos}")

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
                visited.add(guard_pos)
        else:  # Out of bounds
            # Print the coordinates before turning right
            print(f"Exited at: {guard_pos}")

            # Turn right
            if guard_dir == 'U':
                guard_dir = 'R'
            elif guard_dir == 'R':
                guard_dir = 'D'
            elif guard_dir == 'D':
                guard_dir = 'L'
            else:  # guard_dir == 'L'
                guard_dir = 'U'

            break  # Exit the loop when out of bounds

    return len(visited)

if __name__ == "__main__":
    result = get_guard_path()
    print(result)
