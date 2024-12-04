# Gemini conversation: https://g.co/gemini/share/35685c5c8381

def calculate_total_distance(filename):
    """
    Calculates the total distance between two lists of numbers in a file.

    Args:
      filename: The name of the file containing the lists.

    Returns:
      The total distance between the two lists.
    """
    left_list = []
    right_list = []

    with open(filename, 'r') as file:
        for line in file:
            left, right = map(int, line.strip().split())
            left_list.append(left)
            right_list.append(right)

    left_list.sort()
    right_list.sort()

    total_distance = 0
    for left, right in zip(left_list, right_list):
        total_distance += abs(left - right)

    return total_distance

if __name__ == "__main__":
    filename = "input_1.txt"
    total_distance = calculate_total_distance(filename)
    print(f"The total distance between the lists is: {total_distance}")
