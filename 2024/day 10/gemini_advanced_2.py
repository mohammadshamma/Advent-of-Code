# Conversation with Gemini: https://g.co/gemini/share/8e0e07b99a11
# Conversation steps: 1

def find_paths(grid, x, y, visited):
    """
    Recursively finds all paths from a starting point (x, y) to a 9-height position.

    Args:
      grid: The topographic map as a 2D list.
      x: The x-coordinate of the current position.
      y: The y-coordinate of the current position.
      visited: A set of visited coordinates to prevent cycles.

    Returns:
      The number of paths found.
    """
    if (x, y) in visited or not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return 0
    if grid[x][y] == 9:
        return 1

    visited.add((x, y))
    paths = 0
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == grid[x][y] + 1:
            paths += find_paths(grid, new_x, new_y, visited.copy())
    return paths


def calculate_trailhead_ratings(grid):
    """
    Calculates the sum of the ratings of all trailheads on the map.

    Args:
      grid: The topographic map as a 2D list.

    Returns:
      A tuple containing:
        - The sum of the ratings of all trailheads.
        - A list of tuples, each containing a trailhead location (x, y) and its rating.
    """
    total_rating = 0
    ratings = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                rating = find_paths(grid, i, j, set())
                ratings.append(((i, j), rating))
                total_rating += rating
    return total_rating, ratings


def main():
    """
    Reads the input file, processes the data, and prints the result.
    """
    with open("input_1.txt", "r") as file:
        grid = [[int(height) for height in line.strip()] for line in file]
    total_rating, ratings = calculate_trailhead_ratings(grid)
    print("Sum of ratings:", total_rating)
    print("Trailhead ratings:")
    for location, rating in ratings:
        print(f"  {location}: {rating}")

if __name__ == "__main__":
    main()
