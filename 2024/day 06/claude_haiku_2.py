# Claude's artifact: https://claude.site/artifacts/2f3118d7-37a2-418e-9c26-c5a834f4b1a2

def read_input(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def find_starting_position_and_direction(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in '^v<>':
                return x, y, cell
    raise ValueError("No starting position found")

def get_next_direction(current_dir):
    directions = ['^', '>', 'v', '<']
    return directions[(directions.index(current_dir) + 1) % 4]

def is_within_grid(x, y, grid):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def simulate_path(grid, obstacle_x, obstacle_y):
    # Find starting position and direction before modifying grid
    start_x, start_y, start_dir = find_starting_position_and_direction(grid)

    # Make a copy of the grid for simulation
    sim_grid = [row[:] for row in grid]

    # Skip if obstacle would be at starting position
    if (obstacle_x, obstacle_y) == (start_x, start_y):
        return None

    # Add the new obstacle (only if it's not the starting position)
    if sim_grid[obstacle_y][obstacle_x] == '.':
        sim_grid[obstacle_y][obstacle_x] = '#'
    else:
        return None  # Invalid position for obstacle

    # Directions mapping
    dir_moves = {
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1),
        '<': (-1, 0)
    }

    # Track visited positions with their direction
    visited = set()
    path = []
    x, y, current_dir = start_x, start_y, start_dir

    while True:
        # Store current state
        state = (x, y, current_dir)
        path.append(state)

        # Calculate next position
        dx, dy = dir_moves[current_dir]
        new_x, new_y = x + dx, y + dy

        # Check if we're about to leave the grid
        if not is_within_grid(new_x, new_y, grid):
            return None

        # Check if blocked
        if sim_grid[new_y][new_x] == '#':
            current_dir = get_next_direction(current_dir)
        else:
            x, y = new_x, new_y

        # Check for loop
        state = (x, y, current_dir)
        if state in visited:
            # Found a loop
            loop_start = path.index(state)
            return path[loop_start:]
        visited.add(state)

def find_loop_positions(grid):
    loop_positions = set()

    # Try each position in the grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # Skip if position already has an obstacle
            if grid[y][x] == '#':
                continue

            # Try placing obstacle at this position
            loop = simulate_path(grid, x, y)
            if loop is not None:
                loop_positions.add((x, y))

    return loop_positions

def main():
    # Read input from file
    grid = read_input('input_1.txt')

    # Find all positions that create loops
    loop_positions = find_loop_positions(grid)

    print(f"Number of possible positions: {len(loop_positions)}")

if __name__ == "__main__":
    main()
