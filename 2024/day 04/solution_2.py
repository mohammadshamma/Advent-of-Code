# Gemini conversation: https://g.co/gemini/share/b7c44e16c9c1

def find_xmas(grid):
    """
    Finds all occurrences of X-MAS (two MAS in the shape of an X, both diagonal,
    with MAS spelled forwards or backwards) in a grid of letters.

    Args:
      grid: A list of strings representing the word search grid.

    Returns:
      The number of times X-MAS appears in the grid.
    """
    rows, cols = len(grid), len(grid[0])
    count = 0

    def check_xmas(row, col):
        """
        Checks if an X-MAS pattern exists centered at (row, col),
        with both "MAS" formed diagonally (forwards or backwards).
        """
        if 0 <= row - 1 < rows and 0 <= row + 1 < rows and 0 <= col - 1 < cols and 0 <= col + 1 < cols:
            center = grid[row][col]
            top_left = grid[row - 1][col - 1]
            top_right = grid[row - 1][col + 1]
            bottom_left = grid[row + 1][col - 1]
            bottom_right = grid[row + 1][col + 1]

            # Check for two diagonal "MAS" (or "SAM") forming an X
            if (
                (top_left == "M" and center == "A" and bottom_right == "S") or
                (top_left == "S" and center == "A" and bottom_right == "M")
            ) and (
                (top_right == "M" and center == "A" and bottom_left == "S") or
                (top_right == "S" and center == "A" and bottom_left == "M")
            ):
                return True
        return False  # No X-MAS found

    for row in range(rows):
        for col in range(cols):
            if check_xmas(row, col):
                count += 1

    return count

if __name__ == "__main__":
    with open("input_1.txt", "r") as f:
        grid = [line.strip() for line in f]
    count = find_xmas(grid)
    print(count)
