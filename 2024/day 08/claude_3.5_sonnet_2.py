# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/5610c0ea-c3b5-4707-909f-90d767a7388c
# Conversation steps: 2

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

def get_line_points(p1: Tuple[int, int], p2: Tuple[int, int], grid: List[List[str]]) -> Set[Tuple[int, int]]:
    """Get all points that lie on the line through two points in both directions."""
    x1, y1 = p1
    x2, y2 = p2
    points = set()

    # Calculate direction vector
    dx = x2 - x1
    dy = y2 - y1

    # Add points in both positive and negative directions
    for i in range(-len(grid), len(grid) * 2):  # Use grid size as a reasonable range
        x = x1 + dx * i
        y = y1 + dy * i
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            points.add((int(x), int(y)))

    return points

def is_within_bounds(point: Tuple[int, int], grid: List[List[str]]) -> bool:
    """Check if a point is within the grid bounds."""
    x, y = point
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def print_grid(grid: List[List[str]], antennas: defaultdict, antinodes: Set[Tuple[int, int]]):
    """Print the grid showing antennas and antinodes."""
    print("\nOriginal radar locations:")
    for row in grid:
        print(''.join(row))

    print("\nRadar locations by frequency:")
    for freq, positions in sorted(antennas.items()):
        print(f"Frequency {freq}: {positions}")

    print("\nAntinode locations:")
    antinode_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Mark antinodes first (so antennas can override if they're in same position)
    for x, y in antinodes:
        antinode_grid[y][x] = '#'

    # Mark original antennas
    for freq, positions in antennas.items():
        for x, y in positions:
            antinode_grid[y][x] = freq

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
        # If there's more than one antenna of this frequency
        if len(positions) > 1:
            # Check all pairs of antennas with the same frequency
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    antenna1 = positions[i]
                    antenna2 = positions[j]

                    # Get all points on the line through the antennas
                    line_points = get_line_points(antenna1, antenna2, grid)

                    # Add all points to antinodes set
                    antinodes.update(line_points)

    # Print visualizations
    print_grid(grid, antennas, antinodes)

    return len(antinodes)

if __name__ == "__main__":
    result = solve_puzzle("input_1.txt")
    print(f"\nNumber of unique antinode locations: {result}")
