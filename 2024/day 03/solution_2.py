# Gemini conversation: https://g.co/gemini/share/2666f4b1be5e

import re

def calculate_result(input_string):
    """
    Calculates the sum of the results of enabled 'mul' instructions in a string,
    considering 'do()' and "don't()" instructions.

    Args:
      input_string: The string containing instructions.

    Returns:
      The sum of the results of the enabled 'mul' instructions.
    """
    total = 0
    enabled = True  # mul instructions are enabled by default
    pattern = r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))"
    matches = re.findall(pattern, input_string)
    for match in matches:
        if match[0] == "do()":
            enabled = True
        elif match[0] == "don't()":
            enabled = False
        elif enabled:  # Only calculate if mul is enabled
            num1 = int(match[1])
            num2 = int(match[2])
            total += num1 * num2
    return total

if __name__ == "__main__":
    with open("input_1.txt", "r") as file:
        input_string = file.read()
    result = calculate_result(input_string)
    print(result)
