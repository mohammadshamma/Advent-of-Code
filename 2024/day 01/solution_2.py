# Gemini conversation: https://g.co/gemini/share/0431b5ad9242

from collections import Counter

def calculate_similarity_score(filename):
    """
    Calculates the similarity score between two lists of numbers in a file.

    Args:
      filename: The name of the file containing the lists.

    Returns:
      The similarity score between the two lists.
    """
    left_list = []
    right_list = []

    with open(filename, 'r') as file:
        for line in file:
            left, right = map(int, line.strip().split())
            left_list.append(left)
            right_list.append(right)

    right_counts = Counter(right_list)  # Count occurrences in the right list

    similarity_score = 0
    for num in left_list:
        similarity_score += num * right_counts[num]

    return similarity_score

if __name__ == "__main__":
    filename = "input_1.txt"
    similarity_score = calculate_similarity_score(filename)
    print(f"The similarity score between the lists is: {similarity_score}")
