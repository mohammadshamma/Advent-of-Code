# Conversation with ChatGPT: https://chatgpt.com/share/675fc719-77e0-800e-a955-d411b6ceeafa
# Conversation Steps: 1

def read_input(filename="input_1.txt"):
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]
    return grid

def neighbors(r, c, rows, cols):
    # Return valid orthogonal neighbors
    for nr, nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_region(grid, start_r, start_c, visited):
    # BFS/DFS to find all cells in this region of the same type
    rows, cols = len(grid), len(grid[0])
    region_type = grid[start_r][start_c]
    stack = [(start_r, start_c)]
    region_cells = []
    visited[start_r][start_c] = True

    while stack:
        r, c = stack.pop()
        region_cells.append((r,c))
        for nr, nc in neighbors(r, c, rows, cols):
            if not visited[nr][nc] and grid[nr][nc] == region_type:
                visited[nr][nc] = True
                stack.append((nr, nc))

    return region_cells

def calculate_perimeter(grid, region_cells):
    # For each cell in the region, check each side. If out of bounds or different type, add to perimeter.
    region_set = set(region_cells)
    rows, cols = len(grid), len(grid[0])
    region_type = grid[region_cells[0][0]][region_cells[0][1]]
    perimeter = 0
    for (r,c) in region_cells:
        # Up
        if r == 0 or grid[r-1][c] != region_type:
            perimeter += 1
        # Down
        if r == rows - 1 or grid[r+1][c] != region_type:
            perimeter += 1
        # Left
        if c == 0 or grid[r][c-1] != region_type:
            perimeter += 1
        # Right
        if c == cols - 1 or grid[r][c+1] != region_type:
            perimeter += 1
    return perimeter

def main():
    grid = read_input("input_1.txt")
    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]

    total_price = 0
    # Find regions
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region_cells = find_region(grid, r, c, visited)
                area = len(region_cells)
                perimeter = calculate_perimeter(grid, region_cells)
                price = area * perimeter
                total_price += price

    print(total_price)

if __name__ == "__main__":
    main()
