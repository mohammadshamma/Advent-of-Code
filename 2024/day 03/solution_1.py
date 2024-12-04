# Gemini conversation: https://g.co/gemini/share/2177a43deb77

import re

def calculate_result(input_string):
    """
    Calculates the sum of the results of valid 'mul' instructions in a string.

    Args:
      input_string: The string containing potentially corrupted 'mul' instructions.

    Returns:
      The sum of the results of the valid 'mul' instructions.
    """
    total = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"  # Matches valid mul instructions
    matches = re.findall(pattern, input_string)
    for match in matches:
        num1 = int(match[0])
        num2 = int(match[1])
        total += num1 * num2
    return total

if __name__ == "__main__":
    with open("input_1.txt", "r") as file:
        input_string = file.read()
    result = calculate_result(input_string)
    print(result)
