# Conversation with ChatGPT: https://chatgpt.com/share/675e76bb-f798-800e-b884-6919c328da18
# Conversation Steps: 10

memo = {}

def multiply_by_2024(num_str):
    val = int(num_str)
    val *= 2024
    return str(val)

def transform_stone_once(stone):
    """Transform a single stone for one blink."""
    if stone == "0":
        # Rule 1: 0 -> 1
        return ["1"]
    length = len(stone)
    if length % 2 == 0:
        # Rule 2: even length -> split into two stones
        half = length // 2
        left_half = str(int(stone[:half]))   # remove leading zeros
        right_half = str(int(stone[half:]))
        return [left_half, right_half]
    else:
        # Rule 3: odd length and not zero -> multiply by 2024
        return [multiply_by_2024(stone)]

def count_stones_after(stone, blinks):
    # If no more blinks, it remains one stone
    if blinks == 0:
        return 1

    # Check memo
    if (blinks, stone) in memo:
        return memo[(blinks, stone)]

    # Transform this stone once
    next_stones = transform_stone_once(stone)

    # Sum the results for each resulting stone
    total_count = 0
    for ns in next_stones:
        total_count += count_stones_after(ns, blinks - 1)

    memo[(blinks, stone)] = total_count
    return total_count

def main():
    # Read initial stones from input file
    with open("input_1.txt", "r") as f:
        line = f.read().strip()
    stones = line.split()

    blinks = 75  # or any number of blinks needed
    result = 0
    for s in stones:
        result += count_stones_after(s, blinks)

    print(result)

if __name__ == "__main__":
    main()
