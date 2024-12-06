# Conversation with chat GPT: https://chatgpt.com/share/6752cdd9-9318-800e-8f97-b577d9558a0f

def turn_right(direction):
    return (direction + 1) % 4

def simulate(grid, start_r, start_c, start_dir):
    rows = len(grid)
    cols = len(grid[0])
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]

    r, c, d = start_r, start_c, start_dir
    visited_states = set()
    visited_states.add((r, c, d))

    while True:
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc

        # Check if next step is outside the map
        if not (0 <= nr < rows and 0 <= nc < cols):
            # No loop, guard leaves the map
            return False

        # Check if blocked
        if grid[nr][nc] == '#':
            # Turn right
            d = turn_right(d)
        else:
            # Move forward
            r, c = nr, nc
            # Check if we have been here before with the same direction
            if (r, c, d) in visited_states:
                # Loop detected
                return True
            visited_states.add((r, c, d))

def main():
    with open("input_1.txt", "r") as f:
        grid = [list(line.rstrip('\n')) for line in f]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    direction_map = {'^':0, '>':1, 'v':2, '<':3}
    start_r = start_c = None
    start_dir = None

    # Find initial position and direction of the guard
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in direction_map:
                start_dir = direction_map[grid[r][c]]
                start_r, start_c = r, c
                grid[r][c] = '.'  # Replace guard symbol with open space
                break
        if start_dir is not None:
            break

    # If no guard found, no loops can occur
    if start_r is None or start_dir is None:
        print(0)
        return

    # Now we test placing an obstruction in all '.' cells except the guard's starting cell
    loop_count = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) != (start_r, start_c) and grid[r][c] == '.':
                # Place temporary obstruction
                grid[r][c] = '#'
                if simulate(grid, start_r, start_c, start_dir):
                    loop_count += 1
                # Remove obstruction
                grid[r][c] = '.'

    print(loop_count)

if __name__ == "__main__":
    main()
