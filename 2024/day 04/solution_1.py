# Gemini conversation link: https://g.co/gemini/share/2c74e0c99cd8

def find_xmas(grid):
    """
    Finds all occurrences of the word "XMAS" in a grid of letters.

    Args:
      grid: A list of strings representing the word search grid.

    Returns:
      The number of times "XMAS" appears in the grid.
    """
    rows, cols = len(grid), len(grid[0])
    count = 0

    def check_word(row, col, dr, dc):
        """
        Checks if "XMAS" can be formed starting at (row, col) in direction (dr, dc).
        """
        word = ""
        for _ in range(4):
            if 0 <= row < rows and 0 <= col < cols:
                word += grid[row][col]
            else:
                return False
            row += dr
            col += dc
        return word == "XMAS"  # Only check for "XMAS"

    for row in range(rows):
        for col in range(cols):
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr != 0 or dc != 0:  # Avoid checking the same position
                        if check_word(row, col, dr, dc):
                            count += 1

    return count

if __name__ == "__main__":
    with open("input_1.txt", "r") as f:
        grid = [line.strip() for line in f]
    count = find_xmas(grid)
    print(count)
