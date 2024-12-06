# Conversation with Gemini: https://g.co/gemini/share/c46d0b159591

def simulate_guard_path(map_data, obstruction_position):
    """Simulates the guard's path with a given obstruction and returns True if a loop is detected.

    Args:
        map_data: A list of strings representing the map.
        obstruction_position: A tuple (row, col) representing the position of the obstruction.

    Returns:
        True if a loop is detected, False otherwise.
    """

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    current_direction = 0
    current_position = (0, 0)
    visited_positions = set()
    visited_positions.add(((current_position[0], current_position[1]), current_direction))

    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            if map_data[row][col] == '^':
                current_position = (row, col)
                break

    while True:
        next_row, next_col = current_position[0] + directions[current_direction][0], current_position[1] + directions[current_direction][1]

        # Check if the next position is within the grid
        if 0 <= next_row < len(map_data) and 0 <= next_col < len(map_data[0]):
            # Check for a loop before moving to the next position
            if ((next_row, next_col), current_direction) in visited_positions:
                return True

            # Check if the next position is not an obstruction
            if map_data[next_row][next_col] != '#' and (next_row, next_col) != obstruction_position:
                current_position = (next_row, next_col)
                visited_positions.add(((current_position[0], current_position[1]), current_direction))
            else:
                current_direction = (current_direction + 1) % 4
        else:
            # If the next position is out of bounds, return False
            return False

    return False

def find_loop_positions(map_data):
    """Finds all positions where placing an obstruction can create a loop.

    Args:
        map_data: A list of strings representing the map.

    Returns:
        A list of tuples (row, col) representing valid obstruction positions.
    """

    loop_positions = []
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            if map_data[row][col] != '^' and map_data[row][col] != '#':
                obstruction_position = (row, col)
                if simulate_guard_path(map_data, obstruction_position):
                    loop_positions.append(obstruction_position)

    return loop_positions

def main():
    with open('input_1.txt', 'r') as f:
        map_data = f.read().splitlines()

    loop_positions = find_loop_positions(map_data)
    print(len(loop_positions))

if __name__ == '__main__':
    main()
