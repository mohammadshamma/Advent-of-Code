# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/12fbb3d3-67fe-4002-bdc9-7cef75821430
# Conversation steps: 1

def parse_disk_map(disk_map):
    """Convert the dense format into a list of alternating file sizes and free spaces."""
    return [int(x) for x in disk_map]

def create_block_representation(sizes):
    """Convert sizes into a list where each element represents one block."""
    blocks = []
    file_id = 0
    for i, size in enumerate(sizes):
        # Even indices are files, odd indices are free space
        if i % 2 == 0:  # File
            blocks.extend([file_id] * size)
            file_id += 1
        else:  # Free space
            blocks.extend([-1] * size)  # -1 represents free space
    return blocks

def find_rightmost_file_and_leftmost_space(blocks):
    """Find the rightmost file block and leftmost free space that comes before it."""
    rightmost_file_pos = -1
    rightmost_file_id = -1
    leftmost_space_pos = -1

    # Find rightmost file
    for i in range(len(blocks)-1, -1, -1):
        if blocks[i] >= 0:  # It's a file
            rightmost_file_pos = i
            rightmost_file_id = blocks[i]
            break

    # Find leftmost space before this file
    for i in range(rightmost_file_pos):
        if blocks[i] == -1:  # It's a free space
            leftmost_space_pos = i
            break

    return rightmost_file_pos, rightmost_file_id, leftmost_space_pos

def compact_disk(blocks):
    """Move files one block at a time from right to left until no gaps remain."""
    while True:
        right_pos, file_id, left_pos = find_rightmost_file_and_leftmost_space(blocks)

        if left_pos == -1 or right_pos == -1:  # No more moves possible
            break

        # Move one block
        blocks[left_pos] = file_id
        blocks[right_pos] = -1

def calculate_checksum(blocks):
    """Calculate the filesystem checksum."""
    checksum = 0
    for pos, file_id in enumerate(blocks):
        if file_id >= 0:  # Skip free space (-1)
            checksum += pos * file_id
    return checksum

def solve(input_file):
    # Read input
    with open(input_file, 'r') as f:
        disk_map = f.read().strip()

    # Parse input into sizes
    sizes = parse_disk_map(disk_map)

    # Convert to block representation
    blocks = create_block_representation(sizes)

    # Compact the disk
    compact_disk(blocks)

    # Calculate and return checksum
    return calculate_checksum(blocks)

if __name__ == "__main__":
    result = solve("input_1.txt")
    print(f"The filesystem checksum is: {result}")
