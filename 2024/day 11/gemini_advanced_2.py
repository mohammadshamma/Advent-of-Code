# Conversation with the Gemini Advanced: https://g.co/gemini/share/34910fc4069b
# Conversation Steps: 5

from collections import defaultdict

def count_stones(stone, blink_count, memo):
    """
    Recursively counts the number of stones after a given number of blinks
    with memoization.
    """
    key = (stone, blink_count)
    if key in memo:
        return memo[key]

    stone = str(stone)
    if blink_count == 0:
        result = 1  # Base case: no more blinks, count is 1
    elif stone == "0":
        result = count_stones(1, blink_count - 1, memo)
    elif len(stone) % 2 == 0:
        mid = len(stone) // 2
        result = count_stones(int(stone[:mid]), blink_count - 1, memo) + \
                 count_stones(int(stone[mid:]), blink_count - 1, memo)
    else:
        result = count_stones(int(stone) * 2024, blink_count - 1, memo)

    memo[key] = result
    return result

def main():
    """Reads input, simulates blinks with recursive memoization."""
    with open("input_1.txt", "r") as file:
        stones = [int(x) for x in file.readline().split()]

    memo = defaultdict(int)
    blink_count = 75
    total_stones = 0
    for stone in stones:
        total_stones += count_stones(stone, blink_count, memo)

    print(total_stones)

if __name__ == "__main__":
    main()
