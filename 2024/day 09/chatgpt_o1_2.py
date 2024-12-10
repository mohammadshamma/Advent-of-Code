# Conversation with ChatGPT o1: https://chatgpt.com/share/6757a824-4244-800e-b4af-7a6d5aa5c2bb
# Conversation steps: 1

def main():
    with open("input_1.txt", "r") as f:
        disk_map_str = f.read().strip()

    # Parse the disk map into a sequence of blocks
    # The pattern alternates between file_length and free_length.
    lengths = [int(ch) for ch in disk_map_str]

    blocks = []
    file_id = 0
    expecting_file = True
    for length in lengths:
        if length > 0:
            if expecting_file:
                # Add 'length' blocks of the current file_id
                blocks.extend([str(file_id)] * length)
                file_id += 1
            else:
                # Add 'length' free blocks
                blocks.extend(['.'] * length)
        expecting_file = not expecting_file

    # Determine file info: start, end, length for each file_id
    # Since files were appended in order, file IDs start from 0 and go up to file_id-1
    total_files = file_id
    # We'll find ranges for each file by scanning once
    # file_positions[file_id] = (start_index, end_index, length)
    file_positions = [None] * total_files

    # Scan for files:
    # We'll track the first occurrence and last occurrence of each file ID
    first_occ = {}
    last_occ = {}
    for i, b in enumerate(blocks):
        if b != '.':
            fid = int(b)
            if fid not in first_occ:
                first_occ[fid] = i
            last_occ[fid] = i

    for fid in range(total_files):
        start = first_occ[fid]
        end = last_occ[fid]
        length = end - start + 1
        file_positions[fid] = (start, end, length)

    # Now we process files in order of decreasing file ID
    for fid in range(total_files - 1, -1, -1):
        start, end, length = file_positions[fid]

        # Find a contiguous run of '.' that can fit this file to the left of 'start'
        # The run must be entirely before 'start'
        # We'll scan the blocks from left to (start-1) to find a run of '.' of length >= file_length
        # If multiple possible places, we take the leftmost suitable run as the problem states "Attempt to move"
        # It doesn't explicitly say which run if multiple; typically, we would choose the first one we find.
        # If none found, do nothing.

        if start == 0:
            # Can't move further left if it's already at the start
            continue

        # Search for runs of free space
        # We'll do a simple linear scan
        best_start = None
        free_count = 0
        run_start = None
        for i in range(start):
            if blocks[i] == '.':
                if run_start is None:
                    run_start = i
                    free_count = 1
                else:
                    free_count += 1
                # Check if we have enough space
                if free_count == length:
                    # We found a suitable run of exactly the required length
                    best_start = run_start
                    break
                elif free_count > length:
                    # If run is longer than needed, we still can choose its earliest start
                    # Once we found a run that can fit the file, stop searching
                    # The earliest suitable run is what we should pick
                    best_start = run_start
                    break
            else:
                # Reset run
                run_start = None
                free_count = 0

        # If we didn't find a suitable run
        if best_start is None:
            # Can't move this file
            continue

        # We found a run starting at best_start with at least 'length' free blocks
        # Move the file there
        # Steps to move:
        # 1. Save the file blocks
        file_blocks = blocks[start:end+1]

        # 2. Replace the old file location with '.'
        for i in range(start, end+1):
            blocks[i] = '.'

        # 3. Place the file blocks starting at best_start
        for i in range(best_start, best_start+length):
            blocks[i] = file_blocks[i - best_start]

        # Update the file_positions for this file
        new_start = best_start
        new_end = best_start + length - 1
        file_positions[fid] = (new_start, new_end, length)

        # Note: Moving this file might have opened up more free space somewhere else,
        # but we don't need to re-check previous files since we only move each file once.

    # After all files have been considered, compute the checksum
    checksum = 0
    for pos, b in enumerate(blocks):
        if b != '.':
            fid = int(b)
            checksum += pos * fid

    print(checksum)

if __name__ == "__main__":
    main()
