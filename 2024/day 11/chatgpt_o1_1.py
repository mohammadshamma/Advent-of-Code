# Conversation with ChatGPT: https://chatgpt.com/share/675e76bb-f798-800e-b884-6919c328da18
# Conversation Steps: 1

def transform_stones(stones):
    """
    Transforms the list of stones according to the given rules, applied simultaneously.

    Rules:
    1. If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    2. If the stone is engraved with a number that has an even number of digits, it is replaced by two stones:
       - The left half of the digits form the new left stone
       - The right half of the digits form the new right stone
       (Leading zeros are dropped from the halves by converting them to int)
    3. Otherwise (odd number of digits and not zero), the stone is replaced by one stone with its number * 2024.
    """
    new_stones = []
    for stone in stones:
        if stone == 0:
            # Rule 1
            new_stones.append(1)
        else:
            # Convert stone to string to check digit length
            s = str(stone)
            length = len(s)
            if length % 2 == 0:
                # Rule 2: even number of digits
                half = length // 2
                left_half = int(s[:half])
                right_half = int(s[half:])
                new_stones.append(left_half)
                new_stones.append(right_half)
            else:
                # Rule 3: odd number of digits and not zero
                new_stones.append(stone * 2024)
    return new_stones

def main():
    # Read initial stones from input file (assumed space-separated integers on one line)
    with open("input_1.txt", "r") as f:
        line = f.read().strip()
    stones = list(map(int, line.split()))

    # Apply transformations 25 times
    for _ in range(25):
        stones = transform_stones(stones)

    # Print the number of stones after 25 transformations
    print(len(stones))

if __name__ == "__main__":
    main()
