# Conversation with ChatGPT o1: https://chatgpt.com/share/6757a824-4244-800e-b4af-7a6d5aa5c2bb
# Conversation steps: 5

def main():
    # Read the input from "input_1.txt"
    with open("input_1.txt", "r") as f:
        disk_map_str = f.read().strip()

    # Parse the disk map into blocks:
    lengths = [int(ch) for ch in disk_map_str]

    blocks = []
    file_id = 0
    expecting_file = True
    for length in lengths:
        if length > 0:
            if expecting_file:
                # Add file blocks with the current file_id
                blocks.extend([str(file_id)] * length)
                file_id += 1
            else:
                # Add free space
                blocks.extend(['.'] * length)
        expecting_file = not expecting_file

    # Print the initial state
    # print("Initial state:")
    # print("".join(blocks))

    # Simulate the compaction process step by step:
    move_count = 0
    max_moves = 10_000_000  # safeguard for extremely large inputs
    while True:
        try:
            leftmost_dot = blocks.index('.')
        except ValueError:
            # No '.' found, no free space left
            break

        # Find the rightmost file block that occurs after leftmost_dot
        rightmost_file_idx = None
        for idx in range(len(blocks)-1, leftmost_dot, -1):
            if blocks[idx] != '.':
                rightmost_file_idx = idx
                break

        # If we can't find a file block to the right of leftmost_dot, we are done
        if rightmost_file_idx is None:
            break

        # Move that file block to fill the leftmost dot
        file_block = blocks[rightmost_file_idx]
        blocks[leftmost_dot] = file_block
        blocks[rightmost_file_idx] = '.'

        move_count += 1
        # Commenting out the debug prints
        # print(f"After move {move_count}:")
        # print("".join(blocks))

        if move_count > max_moves:
            # print("Reached maximum move count limit, stopping to avoid infinite loop.")
            break

    # After compaction, calculate the checksum
    checksum = 0
    for pos, b in enumerate(blocks):
        if b != '.':
            checksum += pos * int(b)

    print(checksum)

if __name__ == "__main__":
    main()
