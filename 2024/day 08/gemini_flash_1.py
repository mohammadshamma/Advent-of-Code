# Gemini Flash Conversation: https://g.co/gemini/share/0a6f905b7239
# Conversation steps: 8

def count_antinodes(grid):
    """Counts the number of antinodes in a given grid.

    Args:
        grid: A list of lists representing the grid of antennas.

    Returns:
        The number of unique antinode locations.
    """

    height = len(grid)
    width = len(grid[0])
    antinodes = set()

    for y1 in range(height):
        for x1 in range(width):
            freq1 = grid[y1][x1]
            if freq1 == '.':
                continue

            for y2 in range(y1 + 1, height):
                for x2 in range(width):
                    freq2 = grid[y2][x2]
                    if freq2 == '.' or freq1 != freq2:
                        continue

                    dy = y2 - y1
                    dx = x2 - x1

                    new_y1 = y1 - dy
                    new_x1 = x1 - dx
                    new_y2 = y2 + dy
                    new_x2 = x2 + dx

                    if 0 <= new_y1 < height and 0 <= new_x1 < width:
                        antinodes.add((new_y1, new_x1))
                    if 0 <= new_y2 < height and 0 <= new_x2 < width:
                        antinodes.add((new_y2, new_x2))

    return antinodes

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def mark_antinodes(grid, antinodes):
    new_grid = [list(row) for row in grid]
    for y, x in antinodes:
        new_grid[y][x] = '#'
    return new_grid

# Read the input from the file
with open("input_1.txt", "r") as f:
    grid = f.readlines()
    grid = [list(row.strip()) for row in grid]

# Count the antinodes
antinodes = count_antinodes(grid)

# Print the original grid
print("Original Grid:")
print_grid(grid)

# Print the grid with antinodes marked
marked_grid = mark_antinodes(grid, antinodes)
print("\nGrid with Antinodes:")
print_grid(marked_grid)

print("\nNumber of unique antinode locations:", len(antinodes))
