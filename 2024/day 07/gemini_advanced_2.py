# Conversation with Gemini: https://g.co/gemini/share/dbe4fff008a5
# Conversation steps: 1

def evaluate_expression(numbers, operators):
    """Evaluates a list of numbers and operators left-to-right."""
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == "+":
            result += numbers[i + 1]
        elif operators[i] == "*":
            result *= numbers[i + 1]
        elif operators[i] == "||":
            result = int(str(result) + str(numbers[i + 1]))
    return result

def find_valid_equations(filename):
    """
    Reads equations from a file and returns the sum of the test values
    for equations that can be made true with '+', '*', and '||'.
    """
    total = 0
    with open(filename, "r") as file:
        for line in file:
            test_value, numbers_str = line.strip().split(":")
            test_value = int(test_value)
            numbers = [int(x) for x in numbers_str.split()]

            # Generate all possible operator combinations
            num_operators = len(numbers) - 1
            for i in range(3**num_operators):  # 3 operators now
                operators = []
                for j in range(num_operators):
                    op_index = (i // (3**j)) % 3
                    if op_index == 0:
                        operators.append("+")
                    elif op_index == 1:
                        operators.append("*")
                    else:
                        operators.append("||")
                if evaluate_expression(numbers, operators) == test_value:
                    total += test_value
                    break  # Move on to the next equation once a valid combination is found
    return total

if __name__ == "__main__":
    filename = "input_1.txt"
    total_calibration_result = find_valid_equations(filename)
    print(f"Total calibration result: {total_calibration_result}")
