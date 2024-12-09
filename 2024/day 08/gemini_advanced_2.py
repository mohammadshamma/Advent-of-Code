# Gemini Advanced Conversation: https://g.co/gemini/share/03347a88a380
# Conversation step count: 5

def find_antinodes_with_harmonics(grid):
    """
    Calculates the number of unique antinodes in a grid of antennas,
    considering resonant harmonics.

    Args:
      grid: A list of strings representing the antenna layout.

    Returns:
      The number of unique antinode locations.
    """

    rows = len(grid)
    cols = len(grid[0])
    antinodes = set()

    for row in range(rows):
        for col in range(cols):
            freq = grid[row][col]
            if freq == '.':
                continue

            # Check all possible directions
            for dr in range(-rows, rows):
                for dc in range(-cols, cols):
                    if dr == 0 and dc == 0:  # Skip checking the antenna itself
                        continue

                    r, c = row + dr, col + dc
                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == freq:
                        n = 0  # Start searching from n = 0
                        while 0 <= row + n * dr < rows and 0 <= col + n * dc < cols:
                            antinodes.add((row + n * dr, col + n * dc))
                            n += 1

    return antinodes


def print_grid(grid, antinodes):
    """
    Prints the antenna grid and the antinode grid.

    Args:
      grid: A list of strings representing the antenna layout.
      antinodes: A set of tuples representing antinode coordinates.
    """

    rows = len(grid)
    cols = len(grid[0])

    print("Antenna Grid:")
    for row in grid:
        print(row)

    print("\nAntinode Grid:")
    for row in range(rows):
        for col in range(cols):
            if (row, col) in antinodes:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    with open("input_1.txt", "r") as f:
        grid = [line.strip() for line in f]

    antinodes = find_antinodes_with_harmonics(grid)
    print_grid(grid, antinodes)
    print(f"\nThere are {len(antinodes)} unique antinode locations (with harmonics).")
