# Conversation with Gemini: https://g.co/gemini/share/5761b0b3c16b
# Conversation Steps: 8

def read_map(filename="input_1.txt"):
    """Reads the garden map from the input file."""
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f]

def explore_region(row, col, plant_type, visited):
    """Recursively explores a region of the same plant type."""
    if (row, col) in visited or not (0 <= row < len(garden_map) and 0 <= col < len(garden_map[0])):
        return 0, 0

    if garden_map[row][col] != plant_type:
        return 0, 0

    visited.add((row, col))
    area = 1
    perimeter = 4

    # Adjust perimeter for all neighbors before recursive calls
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(garden_map) and 0 <= new_col < len(garden_map[0]) and \
           garden_map[new_row][new_col] == plant_type and (new_row, new_col) in visited:
            perimeter -= 2

    # Now make the recursive calls
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        neighbor_area, neighbor_perimeter = explore_region(new_row, new_col, plant_type, visited)
        area += neighbor_area
        perimeter += neighbor_perimeter

    return area, perimeter

def find_regions(garden_map):
    """Finds all regions of connected plants in the garden map."""
    regions = {}
    visited = set()

    for row in range(len(garden_map)):
        for col in range(len(garden_map[0])):
            if (row, col) not in visited:
                plant_type = garden_map[row][col]
                area, perimeter = explore_region(row, col, plant_type, visited)
                if plant_type not in regions:
                    regions[plant_type] = []
                regions[plant_type].append((area, perimeter))

    return regions

def calculate_total_price(regions):
    """Calculates the total price of fencing all regions."""
    total_price = 0
    for plant_type, region_list in regions.items():
        for area, perimeter in region_list:
            total_price += area * perimeter
    return total_price

if __name__ == "__main__":
    garden_map = read_map()
    regions = find_regions(garden_map)
    total_price = calculate_total_price(regions)
    print(f"The total price of fencing all regions is: {total_price}")
