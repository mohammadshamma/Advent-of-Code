# Claude artifact: https://claude.site/artifacts/365d1019-34dc-4e29-ab66-b0a32a62d150

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

def solve_guard_path(grid):
    # Set to track unique visited positions
    visited = set()

    # Find starting position and direction
    x, y, current_dir = find_starting_position_and_direction(grid)

    # Add starting position
    visited.add((x, y))

    # Directions mapping: up(^), right(>), down(v), left(<)
    dir_moves = {
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1),
        '<': (-1, 0)
    }

    while True:
        # Calculate next position
        dx, dy = dir_moves[current_dir]
        new_x, new_y = x + dx, y + dy

        # Exit if next move is out of grid boundaries
        if not is_within_grid(new_x, new_y, grid):
            break

        # Check if next position is blocked
        if grid[new_y][new_x] == '#':
            # Turn right if blocked
            current_dir = get_next_direction(current_dir)
        else:
            # Move
            x, y = new_x, new_y
            visited.add((x, y))

    return len(visited)

def main():
    # Read input from file
    grid = read_input('input_1.txt')

    # Solve and print result
    result = solve_guard_path(grid)
    print(f"Guard will visit {result} distinct positions")

if __name__ == "__main__":
    main()
