# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/a0a94510-787a-4375-bdfb-caaa076708dd
# Conversation Steps: 1

def transform_stones(stones):
    new_stones = []
    for stone in stones:
        num_str = str(stone)

        # Rule 1: If stone is 0, replace with 1
        if stone == 0:
            new_stones.append(1)

        # Rule 2: If number has even number of digits, split in half
        elif len(num_str) % 2 == 0:
            mid = len(num_str) // 2
            left = int(num_str[:mid])
            right = int(num_str[mid:])
            new_stones.extend([left, right])

        # Rule 3: Otherwise multiply by 2024
        else:
            new_stones.append(stone * 2024)

    return new_stones

def solve_stone_puzzle(filename):
    # Read initial stones from file
    with open(filename) as f:
        stones = [int(x) for x in f.read().strip().split()]

    # Simulate 25 blinks
    for _ in range(25):
        stones = transform_stones(stones)

    return len(stones)

if __name__ == "__main__":
    result = solve_stone_puzzle("input_1.txt")
    print(f"After 25 blinks, there will be {result} stones.")
