# Conversation with Gemini Advanced: https://g.co/gemini/share/af8ecf139f32
# Conversation steps: 3

def find_antinodes(grid):
    """
    Calculates the number of unique antinodes in a grid of antennas.

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
                    if dr == 0 and dc == 0:  # Skip the antenna itself
                        continue

                    r1, c1 = row + dr, col + dc
                    r2, c2 = row + 2 * dr, col + 2 * dc
                    r3, c3 = row - dr, col - dc  # Antinode in the opposite direction

                    if 0 <= r1 < rows and 0 <= c1 < cols and grid[r1][c1] == freq:
                        if 0 <= r2 < rows and 0 <= c2 < cols:
                            antinodes.add((r2, c2))
                        if 0 <= r3 < rows and 0 <= c3 < cols:
                            antinodes.add((r3, c3))

    return len(antinodes)


if __name__ == "__main__":
    with open("input_1.txt", "r") as f:
        grid = [line.strip() for line in f]

    antinode_count = find_antinodes(grid)
    print(f"There are {antinode_count} unique antinode locations.")
