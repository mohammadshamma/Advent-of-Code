# Conversation with ChatGPT: https://chatgpt.com/share/675fc719-77e0-800e-a955-d411b6ceeafa
# Conversation Steps: 8
# Note, the code below solved all samples, but it could not solve the problem input.

def read_input(filename="input_1.txt"):
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]
    return grid

def neighbors(r, c, rows, cols):
    # Return valid orthogonal neighbors (up, down, left, right)
    for nr, nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc

def find_region(grid, start_r, start_c, visited):
    # Perform a DFS to find all cells in the region that share the same plant type
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

def get_boundary_edges(grid, region_cells):
    """
    Given the grid and all cells in a particular region, find all the boundary edges.
    A boundary edge is a segment where the region touches a different region or the edge of the grid.

    Each cell can have up to 4 boundary edges:
    - top:    between (r,c) and (r,c+1)
    - bottom: between (r+1,c) and (r+1,c+1)
    - left:   between (r,c) and (r+1,c)
    - right:  between (r,c+1) and (r+1,c+1)

    If the adjacent cell in that direction is not in region_set or we're at a grid boundary,
    that edge is a boundary edge.
    """
    rows, cols = len(grid), len(grid[0])
    region_set = set(region_cells)
    edges = set()

    for (r,c) in region_cells:
        # Top edge
        if r == 0 or (r-1,c) not in region_set:
            e = ((r,c),(r,c+1))
            if e[0] > e[1]:
                e = (e[1], e[0])
            edges.add(e)
        # Bottom edge
        if r == rows-1 or (r+1,c) not in region_set:
            e = ((r+1,c),(r+1,c+1))
            if e[0] > e[1]:
                e = (e[1], e[0])
            edges.add(e)
        # Left edge
        if c == 0 or (r,c-1) not in region_set:
            e = ((r,c),(r+1,c))
            if e[0] > e[1]:
                e = (e[1], e[0])
            edges.add(e)
        # Right edge
        if c == cols-1 or (r,c+1) not in region_set:
            e = ((r,c+1),(r+1,c+1))
            if e[0] > e[1]:
                e = (e[1], e[0])
            edges.add(e)

    return edges

def build_graph_from_edges(edges):
    """
    Build a graph (adjacency list) from a set of edges.
    Each vertex is a tuple (r,c), and each edge connects two such vertices.
    """
    graph = {}
    for e in edges:
        v1, v2 = e
        if v1 not in graph:
            graph[v1] = []
        if v2 not in graph:
            graph[v2] = []
        graph[v1].append(v2)
        graph[v2].append(v1)
    return graph

def find_cycles_in_graph(graph, edges):
    """
    Find all cycles in the given graph formed by these edges.

    Each cycle represents a closed polygonal boundary.
    We assume well-formed polygons where each edge is part of exactly one cycle.
    """
    edge_set = set(edges)
    visited_edges = set()
    cycles = []

    for e in edge_set:
        if e not in visited_edges:
            # Start a cycle from edge e
            start = e[0]
            cycle_vertices = [e[0], e[1]]
            visited_edges.add(e)
            prev_vertex = e[0]
            current = e[1]

            while True:
                # Find the next vertex different from prev_vertex
                nxt_candidates = [x for x in graph[current] if x != prev_vertex]
                if len(nxt_candidates) != 1:
                    # Not a proper polygon structure if not exactly one candidate
                    break
                nxt = nxt_candidates[0]

                edge_candidate = (current, nxt) if current < nxt else (nxt, current)
                if edge_candidate in visited_edges:
                    # Check if we closed the cycle
                    if nxt == cycle_vertices[0]:
                        # Cycle completed
                        break
                    else:
                        # Unexpected scenario
                        break
                visited_edges.add(edge_candidate)
                cycle_vertices.append(nxt)
                prev_vertex = current
                current = nxt

            cycles.append(cycle_vertices)

    return cycles

def count_sides_in_polygon(cycle_vertices):
    """
    Count how many straight sides a rectilinear polygon has.

    If the polygon is represented with the first vertex repeated at the end, remove it.
    After that, we consider each pair of consecutive edges to determine if there's a change in direction.
    Each direction change corresponds to a corner, and each corner corresponds to a new side.
    """
    # Remove duplicate last vertex if it equals the first vertex
    if cycle_vertices[0] == cycle_vertices[-1]:
        cycle_vertices = cycle_vertices[:-1]

    n = len(cycle_vertices)
    directions = []

    # Determine the direction of each edge
    for i in range(n):
        v1 = cycle_vertices[i]
        v2 = cycle_vertices[(i+1) % n]
        direction = 'H' if v1[0] == v2[0] else 'V'
        directions.append(direction)

    # Count direction changes
    sides = 0
    for i in range(n):
        prev_i = (i - 1) % n
        if directions[i] != directions[prev_i]:
            sides += 1

    return sides

def calculate_sides_for_region(grid, region_cells):
    """
    Calculate the number of sides for a given region.
    This version prints intermediate debug information.
    """
    print("  [Debug] Calculating sides for region:")
    edges = get_boundary_edges(grid, region_cells)
    print("  [Debug] Boundary Edges:")
    for e in sorted(edges):
        print("    ", e)
    print()

    if not edges:
        print("  [Debug] No edges found for this region.")
        return 0

    graph = build_graph_from_edges(edges)
    print("  [Debug] Graph Adjacency List:")
    for v in sorted(graph.keys()):
        print("    ", v, "->", sorted(graph[v]))
    print()

    cycles = find_cycles_in_graph(graph, edges)
    print("  [Debug] Cycles found:")
    for i, cycle in enumerate(cycles, start=1):
        print(f"    Cycle {i}: {cycle}")
    print()

    total_sides = 0
    print("  [Debug] Counting sides for each cycle:")
    for i, cycle in enumerate(cycles, start=1):
        sides = count_sides_in_polygon(cycle)
        print(f"    Cycle {i} sides: {sides}")
        total_sides += sides

    print(f"  [Debug] Total sides for this region: {total_sides}")
    print()
    return total_sides

def main():
    grid = read_input("input_1.txt")
    rows, cols = len(grid), len(grid[0])
    visited = [[False]*cols for _ in range(rows)]

    total_price = 0
    region_count = 0

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                region_cells = find_region(grid, r, c, visited)
                region_count += 1
                area = len(region_cells)
                region_type = grid[region_cells[0][0]][region_cells[0][1]]

                print(f"Region {region_count}:")
                print(f"  Type: {region_type}")
                print(f"  Cells: {region_cells}")
                print(f"  Area: {area}")

                sides = calculate_sides_for_region(grid, region_cells)
                price = area * sides
                print(f"  Price: {price}")
                print()

                total_price += price

    print(f"Total Price: {total_price}")

if __name__ == "__main__":
    main()
