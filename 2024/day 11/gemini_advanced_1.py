# Conversation with the Gemini Advanced: https://g.co/gemini/share/8f2983f274bf
# Conversation Steps: 1

def transform_stones(stones):
    """Transforms a list of stones according to the rules."""
    new_stones = []
    for stone in stones:
        stone = str(stone)
        if stone == "0":
            new_stones.append(1)
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            new_stones.append(int(stone[:mid]))
            new_stones.append(int(stone[mid:]))
        else:
            new_stones.append(int(stone) * 2024)
    return new_stones

def main():
    """Reads input, simulates blinks, and prints the result."""
    with open("input_1.txt", "r") as file:
        stones = [int(x) for x in file.readline().split()]

    for _ in range(25):
        stones = transform_stones(stones)

    print(len(stones))

if __name__ == "__main__":
    main()
