# Gemini Advanced conversation: https://g.co/gemini/share/25031c676a2a
# Conversation steps: 5

def compact_disk(disk_map):
    """
    Compacts the disk map and calculates the checksum.

    Args:
      disk_map: The disk map as a string.

    Returns:
      The checksum of the compacted disk.
    """
    file_sizes = []
    free_space_sizes = []
    current_file_id = 0
    disk_blocks = []

    # Parse the disk map into file and free space sizes
    i = 0
    while i < len(disk_map):
        file_sizes.append(int(disk_map[i]))
        i += 1
        if i < len(disk_map):
            free_space_sizes.append(int(disk_map[i]))
            i += 1

    # Create the initial disk blocks representation
    for i in range(len(file_sizes)):
        disk_blocks.extend([current_file_id] * file_sizes[i])
        if i < len(free_space_sizes):  # Handle potential unevenness
            disk_blocks.extend(["."] * free_space_sizes[i])
        current_file_id += 1

    print("Disk blocks before compacting:", disk_blocks)

    # Compact the disk blocks
    while "." in disk_blocks:
        last_file_block = disk_blocks.pop()
        if last_file_block != ".":
            first_free_space_index = disk_blocks.index(".")
            disk_blocks[first_free_space_index] = last_file_block

    print("Disk blocks after compacting:", disk_blocks)

    # Calculate the checksum
    checksum = 0
    for i, block in enumerate(disk_blocks):
        if block != ".":
            checksum += i * block

    return checksum


with open("input_1.txt", "r") as f:
    disk_map = f.readline().strip()

checksum = compact_disk(disk_map)
print("Checksum:", checksum)
