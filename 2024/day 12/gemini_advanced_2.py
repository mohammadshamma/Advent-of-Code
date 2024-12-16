# Conversation with Gemini: https://g.co/gemini/share/adc5826a2e05
# Conversation Steps: 129
# Note, the code below solved all samples, but it could not solve the problem input.


def read_map(filename="input_1.txt"):
    """Reads the garden map from the input file."""
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f]


def calculate_region_sides(region_points, garden_map):
    """Calculates the total number of sides for a region."""
    if not region_points:
        return 0

    plant_type = garden_map[region_points[0][0]][region_points[0][1]]  # Get plant type from the first point
    print(f"Calculating sides for region with plant type: {plant_type}")  # Print the plant type

    borders = set()
    for row, col in region_points:
        plant_type = garden_map[row][col]
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if not (0 <= new_row < len(garden_map) and 0 <= new_col < len(garden_map[0])) or \
               garden_map[new_row][new_col] != plant_type:
                # Calculate the midway border point
                mid_row = 2 * row + dr
                mid_col = 2 * col + dc
                borders.add((mid_row, mid_col))

    # Sort border points by row then column
    borders = sorted(borders)

    print("Sorted border points:", borders)  # Print the sorted border points

    # Group border points into segments
    segments = []
    visited = set()
    for start_point in borders:
        if start_point not in visited:
            segment = [start_point]
            visited.add(start_point)
            curr_point = start_point

            # Identify the side of the region (corrected logic)
            start_row, start_col = start_point[0], start_point[1]
            if start_point[1] % 2 == 1:  # Odd column, vertical segment
                left_point = (start_row, start_col - 1)
                right_point = (start_row, start_col + 1)
                if 0 <= left_point[0] // 2 < len(garden_map) and 0 <= left_point[1] // 2 < len(garden_map[0]) and \
                   garden_map[left_point[0] // 2][left_point[1] // 2] == plant_type:
                    side = "left"
                else:
                    side = "right"
            else:  # Odd row, horizontal segment
                top_point = (start_row - 1, start_col)
                bottom_point = (start_row + 1, start_col)
                if 0 <= top_point[0] // 2 < len(garden_map) and 0 <= top_point[1] // 2 < len(garden_map[0]) and \
                   garden_map[top_point[0] // 2][top_point[1] // 2] == plant_type:
                    side = "top"
                else:
                    side = "bottom"

            print(f"Starting segment on the {side} side")

            while True:
                for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                    next_point = (curr_point[0] + dr, curr_point[1] + dc)
                    if next_point in borders and next_point not in visited:
                        # Check if the segment crosses over any region points
                        mid_point = ((curr_point[0] + next_point[0]) // 2, (curr_point[1] + next_point[1]) // 2)
                        if mid_point[0] % 2 == 1 or mid_point[1] % 2 == 1:
                            # Check if the region plant type appears on the identified side
                            if side == "left":
                                check_point = (mid_point[0] // 2, (mid_point[1] - 1) // 2)
                            elif side == "right":
                                check_point = (mid_point[0] // 2, (mid_point[1] + 1) // 2)
                            elif side == "top":
                                check_point = ((mid_point[0] - 1) // 2, mid_point[1] // 2)
                            else:  # side == "bottom"
                                check_point = ((mid_point[0] + 1) // 2, mid_point[1] // 2)

                            if 0 <= check_point[0] < len(garden_map) and 0 <= check_point[1] < len(garden_map[0]) and \
                               garden_map[check_point[0]][check_point[1]] == plant_type:
                                segment.append(next_point)
                                visited.add(next_point)
                                curr_point = next_point
                                print(f"Adding point {next_point} to segment")
                                break
                else:
                    # No connected point found, end of segment
                    break
            segments.append(segment)

    print("Segments:", segments)  # Print the segments

    sides = len(segments)  # Number of sides is the number of segments
    return sides


def explore_region(row, col, plant_type, visited, garden_map):
    """Recursively explores a region of the same plant type."""
    if (row, col) in visited or not (0 <= row < len(garden_map) and 0 <= col < len(garden_map[0])):
        return 0, []

    if garden_map[row][col] != plant_type:
        return 0, []

    visited.add((row, col))
    area = 1
    region_points = [(row, col)]

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        neighbor_area, neighbor_region_points = explore_region(new_row, new_col, plant_type, visited, garden_map)
        area += neighbor_area
        region_points.extend(neighbor_region_points)

    return area, region_points


def find_regions(garden_map):
    """Finds all regions of connected plants in the garden map."""
    regions = {}
    visited = set()

    for row in range(len(garden_map)):
        for col in range(len(garden_map[0])):
            if (row, col) not in visited:
                plant_type = garden_map[row][col]
                area, region_points = explore_region(row, col, plant_type, visited, garden_map)
                sides = calculate_region_sides(region_points, garden_map)
                if plant_type not in regions:
                    regions[plant_type] = []
                regions[plant_type].append((area, sides))

    return regions


def calculate_total_price(regions):
    """Calculates the total price of fencing all regions and prints region details."""
    total_price = 0
    for plant_type, region_list in regions.items():
        for i, (area, sides) in enumerate(region_list):
            price = area * sides
            total_price += price
            print(f"Region {i+1} of {plant_type}: Area = {area}, Sides = {sides}, Price = {price}")
    return total_price


if __name__ == "__main__":
    garden_map = read_map()
    regions = find_regions(garden_map)
    total_price = calculate_total_price(regions)
    print(f"\nThe new total price of fencing all regions is: {total_price}")

# [(5, 0), (6, 0), (7, 0), down
# (7, 1), (7, 2), right
# (6, 2), (5, 2), up
# (5, 3), right
# (6, 3), down
# (6, 4), right
# (5, 4), (4, 4), up
# (4, 3), (4, 2), left
# (3, 2), (2, 2), up
# (2, 1), (2, 0), left
# (3, 0), (4, 0), (5, 0)] down
