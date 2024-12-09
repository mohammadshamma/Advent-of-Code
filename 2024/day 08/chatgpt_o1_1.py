# Conversation with ChatGPT o1: https://chatgpt.com/share/67566628-5728-800e-bf9d-85c3d03db27f
# Conversation steps: 1

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
            # Antennas are single lowercase letter, uppercase letter, or digit
            # '.' indicates no antenna
            if ch != '.':
                if ch not in antennas_by_freq:
                    antennas_by_freq[ch] = []
                antennas_by_freq[ch].append((r, c))

    # For each frequency group, for each pair of antennas, compute the antinodes
    # Antinodes for a pair A=(r1,c1), B=(r2,c2) are given by:
    # Antinode1 = (2*r1 - r2, 2*c1 - c2)
    # Antinode2 = (2*r2 - r1, 2*c2 - c1)
    # This comes from the condition that one antenna is twice as far from the point as the other.
    # These points are on the line through A and B but outside the segment.
    antinodes = set()
    for freq, positions in antennas_by_freq.items():
        n = len(positions)
        if n < 2:
            # Need at least two antennas of same frequency to form antinodes
            continue
        # Consider all pairs
        for i in range(n):
            r1, c1 = positions[i]
            for j in range(i+1, n):
                r2, c2 = positions[j]

                # Compute the two antinodes
                # Antinode1 = 2A - B
                a1r = 2*r1 - r2
                a1c = 2*c1 - c2
                # Antinode2 = 2B - A
                a2r = 2*r2 - r1
                a2c = 2*c2 - c1

                # If they fall within the map, record them
                if 0 <= a1r < rows and 0 <= a1c < cols:
                    antinodes.add((a1r, a1c))
                if 0 <= a2r < rows and 0 <= a2c < cols:
                    antinodes.add((a2r, a2c))

    # The result is the number of unique antinode positions within the map
    print(len(antinodes))


if __name__ == "__main__":
    main()
