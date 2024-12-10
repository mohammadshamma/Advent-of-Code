# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/62170e74-7e02-43b0-b0fc-436c0e37c29e
# Conversation steps: 1

def parse_disk_map(disk_map):
    """Convert the dense format into a list of alternating file sizes and free spaces."""
    return [int(x) for x in disk_map]

def create_block_representation(sizes):
    """Convert sizes into a list where each element represents one block."""
    blocks = []
    file_id = 0
    for i, size in enumerate(sizes):
        # Even indices are files, odd indices are free spaces
        if i % 2 == 0:  # File
            blocks.extend([file_id] * size)
            file_id += 1
        else:  # Free space
            blocks.extend([-1] * size)  # -1 represents free space
    return blocks

def get_file_info(blocks):
    """Get information about each file's position and size."""
    file_info = {}  # {file_id: (start_pos, size)}
    current_id = None
    start_pos = None
    size = 0

    for pos, block_id in enumerate(blocks):
        if block_id != current_id:
            if current_id is not None and current_id >= 0:
                file_info[current_id] = (start_pos, size)
            current_id = block_id
            start_pos = pos
            size = 1
        else:
            size += 1

    # Don't forget the last file
    if current_id is not None and current_id >= 0:
        file_info[current_id] = (start_pos, size)

    return file_info

def find_best_free_space(blocks, file_size, max_pos):
    """Find the leftmost span of free space before max_pos that can fit the file."""
    current_span = 0
    best_start = -1

    for pos in range(max_pos):
        if blocks[pos] == -1:
            if current_span == 0:
                start = pos
            current_span += 1
            if current_span >= file_size:
                best_start = start
                break
        else:
            current_span = 0

    return best_start

def move_file(blocks, start_pos, size, new_pos):
    """Move a file from start_pos to new_pos."""
    file_id = blocks[start_pos]
    # Clear old position
    for i in range(start_pos, start_pos + size):
        blocks[i] = -1
    # Set new position
    for i in range(new_pos, new_pos + size):
        blocks[i] = file_id

def compact_disk_whole_files(blocks):
    """Compact disk by moving whole files from highest ID to lowest."""
    file_info = get_file_info(blocks)

    # Process files in decreasing order of ID
    for file_id in sorted(file_info.keys(), reverse=True):
        start_pos, size = file_info[file_id]
        # Find best free space before current position
        new_pos = find_best_free_space(blocks, size, start_pos)

        if new_pos != -1:  # If we found a suitable space
            move_file(blocks, start_pos, size, new_pos)

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

    # Compact the disk using whole file movement
    compact_disk_whole_files(blocks)

    # Calculate and return checksum
    return calculate_checksum(blocks)

if __name__ == "__main__":
    result = solve("input_1.txt")
    print(f"The filesystem checksum is: {result}")
