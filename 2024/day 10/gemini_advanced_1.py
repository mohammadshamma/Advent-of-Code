# Conversation with Gemini: https://g.co/gemini/share/8e0e07b99a11
# Conversation steps: 9

def find_paths(grid, x, y, visited, nines_found):
    """
    Recursively finds all paths from a starting point (x, y) to 9-height positions.

    Args:
      grid: The topographic map as a 2D list.
      x: The x-coordinate of the current position.
      y: The y-coordinate of the current position.
      visited: A set of visited coordinates to prevent cycles.
      nines_found: A set to keep track of the 9s found from this trailhead.

    Returns:
      None. Modifies the nines_found set in place.
    """
    if (x, y) in visited or not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
        return
    if grid[x][y] == 9:
        nines_found.add((x, y))  # Add the 9's location to the set
        draw_grid(grid, visited, x, y)  # Draw the grid with the path and 9 location
        return

    visited.add((x, y))
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == grid[x][y] + 1:
            find_paths(grid, new_x, new_y, visited.copy(), nines_found)


def draw_grid(grid, visited, nine_x, nine_y):
    """
    Draws the grid with the path marked by elevation values and the location of 9.

    Args:
      grid: The topographic map as a 2D list.
      visited: A set of visited coordinates.
      nine_x: The x-coordinate of the 9.
      nine_y: The y-coordinate of the 9.
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) == (nine_x, nine_y):
                print("9", end="")  # Mark the 9
            elif (i, j) in visited:
                print(grid[i][j], end="")  # Print the elevation value
            else:
                print(".", end="")
        print()
    print()  # Print an empty line to separate the grids


def calculate_trailhead_scores(grid):
    """
    Calculates the sum of the scores of all trailheads on the map and returns a list of individual scores.

    Args:
      grid: The topographic map as a 2D list.

    Returns:
      A tuple containing:
        - The sum of the scores of all trailheads.
        - A list of tuples, each containing a trailhead location (x, y) and its score.
    """
    total_score = 0
    scores = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                nines_found = set()  # Keep track of the 9s found from this trailhead
                find_paths(grid, i, j, set(), nines_found)
                score = len(nines_found)  # Score is the number of unique 9s found
                scores.append(((i, j), score))
                total_score += score
    return total_score, scores


def main():
    """
    Reads the input file, processes the data, and prints the result.
    """
    with open("input_1.txt", "r") as file:
        grid = [[int(height) for height in line.strip()] for line in file]
    total_score, scores = calculate_trailhead_scores(grid)
    print("Sum of scores:", total_score)
    print("Trailhead scores:")
    for location, score in scores:
        print(f"  {location}: {score}")

if __name__ == "__main__":
    main()
