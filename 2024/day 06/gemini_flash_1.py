
# Conversation with Gemini: https://g.co/gemini/share/886f86883270

def simulate_guard_path(map_data):
    """Simulates the guard's path and returns the number of distinct positions visited.

    Args:
        map_data: A list of strings representing the map.

    Returns:
        The number of distinct positions visited by the guard.
    """

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    current_direction = 0
    current_position = (0, 0)
    visited_positions = set()
    visited_positions.add(current_position)

    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            if map_data[row][col] == '^':
                current_position = (row, col)
                break

    while True:
        next_row, next_col = current_position[0] + directions[current_direction][0], current_position[1] + directions[current_direction][1]

        # Check if the next position is within the grid
        if 0 <= next_row < len(map_data) and 0 <= next_col < len(map_data[0]):
            if map_data[next_row][next_col] == '.':
                current_position = (next_row, next_col)
                visited_positions.add(current_position)
            else:
                current_direction = (current_direction + 1) % 4
        else:
            # Guard has exited the grid
            break

    return len(visited_positions)

def main():
    with open('input_1.txt', 'r') as f:
        map_data = f.read().splitlines()

    num_positions = simulate_guard_path(map_data)
    print(num_positions)

if __name__ == '__main__':
    main()
