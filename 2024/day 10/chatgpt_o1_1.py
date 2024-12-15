# Conversation with ChatGPT: https://chatgpt.com/share/675e67bf-cac8-800e-89e6-2b5b8bdae8ec
# Conversation steps: 1

def neighbors(r, c, rows, cols):
    for nr, nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_reachable_nines(r, c, grid, memo):
    # If cached, return the stored result
    if (r, c) in memo:
        return memo[(r, c)]

    h = grid[r][c]
    # If this position is height 9, reachable set is just itself
    if h == 9:
        memo[(r, c)] = {(r, c)}
        return memo[(r, c)]

    # Otherwise, we try to move to neighbors with h+1
    result = set()
    target_height = h + 1
    rows = len(grid)
    cols = len(grid[0])
    for nr, nc in neighbors(r, c, rows, cols):
        if grid[nr][nc] == target_height:
            # Union all sets reachable from these neighbors
            result |= find_reachable_nines(nr, nc, grid, memo)
    memo[(r, c)] = result
    return result

def main():
    # Read the grid from input file
    with open("input_1.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    grid = [list(map(int, list(line))) for line in lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Identify all trailheads (height 0)
    trailheads = [(r,c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    # Memoization dictionary: key=(r,c), value=set of reachable 9 positions
    memo = {}

    total_score = 0
    for r, c in trailheads:
        reachable = find_reachable_nines(r, c, grid, memo)
        # Score is the number of distinct 9-positions reachable
        total_score += len(reachable)

    print(total_score)

if __name__ == "__main__":
    main()
