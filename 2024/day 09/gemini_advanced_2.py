# Gemini Advanced conversation: https://g.co/gemini/share/c4c73bfcfd64
# Conversation steps: 16

def compact_disk_by_file_sparse_merge_free_space(disk_map):
    """
    Compacts the disk map by moving whole files using a sparse representation,
    adds new free space after moving, merges adjacent free spaces, prints
    intermediate steps and variables, and calculates the checksum.

    Args:
      disk_map: The disk map as a string.

    Returns:
      The checksum of the compacted disk.
    """
    files = []  # List to store (start_position, size, file_id) for each file
    free_spaces = []  # List to store (start_position, size) for each free space
    current_position = 0
    current_file_id = 0

    # Parse the disk map into sparse representation
    i = 0
    while i < len(disk_map):
        file_size = int(disk_map[i])
        files.append((current_position, file_size, current_file_id))  # Store file_id
        current_position += file_size
        current_file_id += 1  # Increment file_id after processing a file
        i += 1
        if i < len(disk_map):
            free_space_size = int(disk_map[i])
            free_spaces.append((current_position, free_space_size))
            current_position += free_space_size
            i += 1

    print("Initial files:", files)
    print("Initial free spaces:", free_spaces)

    # Compact the disk by moving whole files
    for file_id in range(len(files) - 1, -1, -1):
        file_start, file_size, file_id = files[file_id]  # Extract file_id
        for i, (free_start, free_size) in enumerate(free_spaces):
            if free_size >= file_size and free_start < file_start:
                # Print variables before moving
                # print("Moving file", file_id)
                # print("  file_size:", file_size)
                # print("  free_space_start:", free_start)
                # print("  free_space_count:", free_size)

                # Move the file
                files[file_id] = (free_start, file_size, file_id)  # Keep file_id
                free_spaces[i] = (free_start + file_size, free_size - file_size)

                # Add new free space at the original location
                free_spaces.append((file_start, file_size))

                # Sort free spaces by start position
                free_spaces.sort()

                # Merge adjacent free spaces
                j = 0
                while j < len(free_spaces) - 1:
                    current_start, current_size = free_spaces[j]
                    next_start, next_size = free_spaces[j + 1]
                    if current_start + current_size == next_start:
                        free_spaces[j] = (current_start, current_size + next_size)
                        del free_spaces[j + 1]
                    else:
                        j += 1

                # print("Files after moving:", files)
                # print("Free spaces after moving:", free_spaces)
                break

    # Calculate the checksum (individual file contributions)
    checksum = 0
    for file_start, file_size, file_id in files:
        for i in range(file_start, file_start + file_size):
            checksum += i * file_id

    return checksum


with open("input_1.txt", "r") as f:
    disk_map = f.readline().strip()

checksum = compact_disk_by_file_sparse_merge_free_space(disk_map)
print("Checksum:", checksum)
