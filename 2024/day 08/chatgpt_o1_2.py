# Conversation with ChatGPT o1: https://chatgpt.com/share/67566628-5728-800e-bf9d-85c3d03db27f
# Conversation steps: 1

from math import gcd

def main():
    # Read the input map from file
    with open("input_1.txt", "r") as f:
        grid = [line.rstrip('\n') for line in f]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Find all antennas and group them by their frequency
    antennas_by_freq = {}
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch != '.':
                antennas_by_freq.setdefault(ch, []).append((r, c))

    antinodes = set()

    for freq, positions in antennas_by_freq.items():
        # If there's fewer than two antennas of this frequency, no line can be formed
        if len(positions) < 2:
            continue

        n = len(positions)
        # For each pair of antennas of the same frequency:
        for i in range(n):
            r1, c1 = positions[i]
            for j in range(i+1, n):
                r2, c2 = positions[j]

                dr = r2 - r1
                dc = c2 - c1
                g = gcd(dr, dc)
                dR = dr // g
                dC = dc // g

                # Now we have a parametric representation of the line:
                # (r, c) = (r1 + k*dR, c1 + k*dC)
                # We need to find all k such that the point is in the grid.

                # Solve for row bounds:
                # 0 <= r1 + k*dR < rows
                row_min_k, row_max_k = None, None
                if dR == 0:
                    # Line is horizontal, so row doesn't restrict k if r1 is valid
                    if 0 <= r1 < rows:
                        # Any k is allowed by row constraint from a row standpoint,
                        # but effectively infinite. We'll rely on columns to restrict.
                        # Let's represent infinite range as None.
                        row_min_k, row_max_k = None, None
                    else:
                        # No points on this line will be inside the grid (invalid row)
                        continue
                else:
                    # dR > 0 or < 0
                    # 0 <= r1 + k*dR < rows
                    # For the lower bound:
                    # r1 + k*dR >= 0 => k*dR >= -r1
                    # For upper bound:
                    # r1 + k*dR < rows => k*dR < rows - r1
                    if dR > 0:
                        min_k_row = -r1 / dR
                        max_k_row = (rows - 1 - r1) / dR
                    else:
                        # dR < 0
                        # Reversing inequalities:
                        min_k_row = (rows - 1 - r1) / dR
                        max_k_row = -r1 / dR

                    # Since k must be integer, we must take ceil for min and floor for max
                    from math import ceil, floor
                    row_min_k = ceil(min_k_row)
                    row_max_k = floor(max_k_row)

                # Solve for column bounds:
                # 0 <= c1 + k*dC < cols
                col_min_k, col_max_k = None, None
                if dC == 0:
                    # Line is vertical
                    if 0 <= c1 < cols:
                        # Any k is allowed by column from this standpoint
                        col_min_k, col_max_k = None, None
                    else:
                        # No valid column intersection
                        continue
                else:
                    if dC > 0:
                        min_k_col = -c1 / dC
                        max_k_col = (cols - 1 - c1) / dC
                    else:
                        min_k_col = (cols - 1 - c1) / dC
                        max_k_col = -c1 / dC

                    from math import ceil, floor
                    col_min_k = ceil(min_k_col)
                    col_max_k = floor(max_k_col)

                # Intersect the row and column k-ranges
                # If either is None, treat as infinite in that direction
                def intersect_ranges(a_min, a_max, b_min, b_max):
                    # Both ranges could be (None, None), meaning infinite
                    # If one range is infinite (None), the other defines the intersection
                    # If both are infinite, intersection is infinite
                    min_k = a_min if a_min is not None else b_min
                    max_k = a_max if a_max is not None else b_max
                    if a_min is not None and b_min is not None:
                        min_k = max(a_min, b_min)
                    if a_max is not None and b_max is not None:
                        max_k = min(a_max, b_max)

                    return min_k, max_k

                min_k, max_k = intersect_ranges(row_min_k, row_max_k, col_min_k, col_max_k)

                # If min_k or max_k are None, that means infinite in that direction
                # But the grid is finite, and min_k/max_k must be finite for actual points.
                # If both are None, that would mean all points in infinite line are valid,
                # but this can't happen since the grid is finite. Actually, it can happen
                # if the line is inside the grid only at one row/col, handled above.
                if min_k is None and max_k is None:
                    # Means line doesn't impose any finite limit from row or column?
                    # Actually this would mean we never restricted k. But since the grid is finite,
                    # we must find at least one direction that restricts. If both dR and dC are zero
                    # that can't happen (no line). If one is zero, we handled that logic above.
                    # Let's handle a scenario: horizontal line inside grid row and column also always inside?
                    # Actually, if dR=0 and the line's row is inside the grid, that doesn't limit k by row,
                    # If also dC=0 that can't happen since no line formed. If dC=0 and c1 fixed column inside grid,
                    # It's just one point line. That's already handled as no restrictions. Just that one point.

                    # If dR=0 (horizontal line):
                    if dR == 0:
                        # Entire row r1 is valid, but we must intersect with column constraints:
                        # If col_min_k and col_max_k were None and we got here, means infinite columns too.
                        # Actually a pure horizontal line (dR=0) inside a single row can't have no column restriction,
                        # because if dC=0, line reduces to a single point. If dC != 0 and we got no column restriction,
                        # that means infinite line horizontally. But the grid is finite. Actually, if dC !=0 and no col_min_k or col_max_k,
                        # means c1 also inside. Check if col_min_k and col_max_k are None? Then we must find them.
                        # If dC=0 but we've returned continue if no good?
                        # Let's handle gracefully:
                        # If we truly have no restriction:
                        # the line is horizontal or vertical and fully inside the grid dimension?
                        # Actually if dR=0, line is horizontal at row=r1.
                        # The column must vary: c = c1 + k*dC
                        # If dC=0 also, no line is formed. If no column restriction found, it means:
                        # c1 within [0, cols-1], stepping by dC=0 would not form a line. If dC=0 can't happen.
                        continue

                    # If dC=0 (vertical line):
                    if dC==0:
                        # Entire column c1 is valid. Similarly as above reasoning.
                        continue

                    # If we got here with no range, something is off, just continue
                    continue

                if min_k is None:
                    # Means only max_k is known
                    # If dR or dC !=0 we need at least one bound. Without a min_k,
                    # we must set a min_k. The line extends infinitely in negative or positive directions.
                    # We can pick an arbitrary large negative number as min_k if max_k is finite.
                    # But that might create huge iteration. Let's reason:
                    # If min_k is None and max_k is finite, it means we didn't get a lower bound from the grid.
                    # This can happen if line is going "out of the grid" in one direction but not in the other.
                    # To handle safely, let's pick a large negative number that ensures no overhead:
                    # Actually, we can find the direction of the line to guess in which direction we must limit k.
                    # Simpler approach: The grid is finite, so at some point going in negative k direction we will leave the grid in either row or column dimension.
                    # But since min_k is None, that means no lower limit from row or col?
                    # Actually, we must have at least one direction giving a lower limit.
                    # If none gave a lower limit, that means line enters the grid from negative infinity?
                    # The line must come from outside the grid. Let's set min_k = -10_000_000 and rely on intersection,
                    # but that might break large. Let's do a more reasoned approach:
                    # Actually, since the grid size is finite, let's just pick min_k = -max(rows, cols) and max_k = max_k from intersection.
                    min_k = -max(rows, cols)*10  # big enough negative number to cover entire grid crossing
                if max_k is None:
                    # Similarly pick a large positive number
                    max_k = max(rows, cols)*10

                # Ensure min_k <= max_k
                if min_k > max_k:
                    continue

                # Now iterate over k in that range
                for k in range(min_k, max_k+1):
                    rr = r1 + k*dR
                    cc = c1 + k*dC
                    if 0 <= rr < rows and 0 <= cc < cols:
                        antinodes.add((rr, cc))

    print(len(antinodes))

if __name__ == "__main__":
    main()
