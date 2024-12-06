# Conversation with chat GPT: https://chatgpt.com/share/6752cdd9-9318-800e-8f97-b577d9558a0f

def turn_right(direction):
    # direction is an index into this list
    # 0: up, 1: right, 2: down, 3: left
    return (direction + 1) % 4

def main():
    with open("input_1.txt", "r") as f:
        grid = [list(line.rstrip('\n')) for line in f]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Find initial position and direction of the guard
    # Directions: 0=up, 1=right, 2=down, 3=left
    direction_map = {'^':0, '>':1, 'v':2, '<':3}
    start_r = start_c = None
    direction = None

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in direction_map:
                direction = direction_map[grid[r][c]]
                start_r, start_c = r, c
                grid[r][c] = '.'  # Replace guard symbol with open space
                break
        if direction is not None:
            break

    # If no guard found, no positions visited
    if start_r is None or direction is None:
        print(0)
        return

    # Directions vectors for up, right, down, left
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]

    visited = set()
    current_r, current_c = start_r, start_c
    visited.add((current_r, current_c))

    while True:
        dr, dc = dirs[direction]
        next_r, next_c = current_r + dr, current_c + dc

        # Check if next step is outside the map
        if not (0 <= next_r < rows and 0 <= next_c < cols):
            # Guard leaves the map
            break

        # Check if next cell is blocked
        if grid[next_r][next_c] == '#':
            # Turn right
            direction = turn_right(direction)
            # Do not move this turn, try again
        else:
            # Move forward
            current_r, current_c = next_r, next_c
            visited.add((current_r, current_c))

    print(len(visited))

if __name__ == "__main__":
    main()
