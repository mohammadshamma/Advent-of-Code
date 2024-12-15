# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/42a8bc86-a799-45e9-9eba-a764e93c6c7c
# Conversation Steps: 1

from collections import deque
from typing import List, Set, Tuple

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

def count_reachable_nines(grid: List[List[int]], start_x: int, start_y: int) -> int:
    """
    Count how many positions with height 9 can be reached from the given starting position
    following valid hiking trails (increasing by exactly 1 at each step).
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    reachable_nines = set()

    def bfs_with_height_check(start_pos: Tuple[int, int]) -> None:
        queue = deque([(start_pos, grid[start_pos[0]][start_pos[1]])])
        while queue:
            (x, y), current_height = queue.popleft()

            if current_height == 9:
                reachable_nines.add((x, y))
                continue

            for next_x, next_y in get_neighbors(x, y, rows, cols):
                next_pos = (next_x, next_y)
                next_height = grid[next_x][next_y]

                if (next_pos not in visited and
                    next_height == current_height + 1):
                    visited.add(next_pos)
                    queue.append((next_pos, next_height))

    bfs_with_height_check((start_x, start_y))
    return len(reachable_nines)

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
    3. For each trailhead, count reachable nines
    4. Return the sum of all scores
    """
    # Read input
    grid = read_input(filename)

    # Find all trailheads
    trailheads = find_trailheads(grid)

    # Calculate score for each trailhead
    total_score = 0
    for x, y in trailheads:
        score = count_reachable_nines(grid, x, y)
        total_score += score

    return total_score

if __name__ == "__main__":
    result = solve_puzzle("input_1.txt")
    print(f"The sum of the scores of all trailheads is: {result}")
