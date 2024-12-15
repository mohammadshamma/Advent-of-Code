# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/84e9eac7-3c51-412e-ae16-6bb77575d21c
# Conversation Steps: 1

from collections import defaultdict, deque
from typing import List, Set, Tuple, Dict

def read_input(filename: str) -> List[List[int]]:
    """Read and parse the input file into a 2D grid of integers."""
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                grid.append([int(c) for c in line.strip()])
    return grid

def get_neighbors(x: int, y: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """Get valid neighboring positions (up, down, left, right)."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    neighbors = []
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols:
            neighbors.append((new_x, new_y))
    return neighbors

def count_distinct_paths(grid: List[List[int]], start_x: int, start_y: int) -> int:
    """
    Count the number of distinct hiking trails from a trailhead.
    Uses dynamic programming to handle multiple paths to the same position.
    """
    rows, cols = len(grid), len(grid[0])
    # Dictionary to store number of paths to each position at each height
    paths = defaultdict(int)
    paths[(start_x, start_y, 0)] = 1  # Starting position has 1 path

    # Process each height level from 0 to 8
    total_paths = 0
    for height in range(9):
        # Find all positions at current height that have paths to them
        current_positions = {(x, y) for (x, y, h) in paths.keys() if h == height}

        for x, y in current_positions:
            current_paths = paths[(x, y, height)]

            # For each neighbor that's exactly one height higher
            for next_x, next_y in get_neighbors(x, y, rows, cols):
                if grid[next_x][next_y] == height + 1:
                    paths[(next_x, next_y, height + 1)] += current_paths

                    # If we've reached height 9, add these paths to total
                    if height + 1 == 9:
                        total_paths += current_paths

    return total_paths

def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Find all positions with height 0 (trailheads)."""
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    return trailheads

def solve_puzzle(filename: str) -> int:
    """
    Main function to solve the puzzle:
    1. Read the input
    2. Find all trailheads
    3. For each trailhead, count distinct paths to any 9
    4. Return the sum of all ratings
    """
    # Read input
    grid = read_input(filename)

    # Find all trailheads
    trailheads = find_trailheads(grid)

    # Calculate rating for each trailhead
    total_rating = 0
    for x, y in trailheads:
        rating = count_distinct_paths(grid, x, y)
        total_rating += rating

    return total_rating

if __name__ == "__main__":
    result = solve_puzzle("input_1.txt")
    print(f"The sum of the ratings of all trailheads is: {result}")
