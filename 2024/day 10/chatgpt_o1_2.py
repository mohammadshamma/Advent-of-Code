# Conversation with ChatGPT: https://chatgpt.com/share/675e67bf-cac8-800e-89e6-2b5b8bdae8ec
# Conversation steps: 1

def neighbors(r, c, rows, cols):
    for nr, nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def count_paths(r, c, grid, memo):
    if (r, c) in memo:
        return memo[(r, c)]

    h = grid[r][c]
    # If height is 9, exactly one path (itself)
    if h == 9:
        memo[(r, c)] = 1
        return 1

    rows = len(grid)
    cols = len(grid[0])
    total_paths = 0
    target_height = h + 1

    for nr, nc in neighbors(r, c, rows, cols):
        if grid[nr][nc] == target_height:
            total_paths += count_paths(nr, nc, grid, memo)

    memo[(r, c)] = total_paths
    return total_paths

def main():
    # Read the grid from input file
    with open("input_1.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    grid = [list(map(int, list(line))) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Identify trailheads (height 0)
    trailheads = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    # Memo for paths
    memo = {}

    total_rating = 0
    for r, c in trailheads:
        total_rating += count_paths(r, c, grid, memo)

    print(total_rating)

if __name__ == "__main__":
    main()
