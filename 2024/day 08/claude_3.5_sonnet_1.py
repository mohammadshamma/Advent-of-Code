# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/0e2eb547-9856-4ba2-86cd-afe02c54fec6
# Conversation steps: 3

from collections import defaultdict
from typing import List, Set, Tuple

def read_input(filename: str) -> List[List[str]]:
    """Read the input file and return as 2D grid."""
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def find_antennas(grid: List[List[str]]) -> defaultdict:
    """Find all antennas and group them by frequency."""
    antennas = defaultdict(list)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] not in '.':
                antennas[grid[y][x]].append((x, y))
    return antennas

def calculate_antinodes(antenna1: Tuple[int, int], antenna2: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Calculate antinode positions for a pair of antennas."""
    x1, y1 = antenna1
    x2, y2 = antenna2

    # Calculate vector between antennas
    dx = x2 - x1
    dy = y2 - y1

    # Calculate antinode positions
    antinode1 = (x1 - dx, y1 - dy)  # One antinode before first antenna
    antinode2 = (x2 + dx, y2 + dy)  # One antinode after second antenna

    return [antinode1, antinode2]

def is_within_bounds(point: Tuple[int, int], grid: List[List[str]]) -> bool:
    """Check if a point is within the grid bounds."""
    x, y = point
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def print_grid(grid: List[List[str]], antennas: defaultdict, antinodes: Set[Tuple[int, int]]):
    """Print the grid showing antennas and antinodes."""
    print("\nOriginal radar locations:")
    # Print original grid
    for row in grid:
        print(''.join(row))

    print("\nRadar locations by frequency:")
    for freq, positions in antennas.items():
        print(f"Frequency {freq}: {positions}")

    print("\nAntinode locations:")
    # Create a new grid with antinodes marked
    antinode_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Mark original antennas
    for freq, positions in antennas.items():
        for x, y in positions:
            antinode_grid[y][x] = freq

    # Mark antinodes
    for x, y in antinodes:
        if antinode_grid[y][x] == '.':
            antinode_grid[y][x] = '#'

    # Print the grid with antinodes
    for row in antinode_grid:
        print(''.join(row))

def solve_puzzle(filename: str) -> int:
    # Read input
    grid = read_input(filename)

    # Find all antennas grouped by frequency
    antennas = find_antennas(grid)

    # Set to store unique antinode positions
    antinodes = set()

    # For each frequency
    for freq, positions in antennas.items():
        # Check all pairs of antennas with the same frequency
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                antenna1 = positions[i]
                antenna2 = positions[j]

                # Calculate antinodes for this pair
                possible_antinodes = calculate_antinodes(antenna1, antenna2)

                # Add antinodes that are within bounds
                for antinode in possible_antinodes:
                    if is_within_bounds(antinode, grid):
                        antinodes.add(antinode)

    # Print visualizations
    print_grid(grid, antennas, antinodes)

    return len(antinodes)

if __name__ == "__main__":
    result = solve_puzzle("input_1.txt")
    print(f"\nNumber of unique antinode locations: {result}")
