# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/32ffe499-84a2-4025-a4ec-c69a25600059
# Conversation steps: 1

from itertools import product

def evaluate_expression(numbers, operators):
    """Evaluate expression left-to-right with given numbers and operators."""
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += numbers[i + 1]
        elif operators[i] == '*':
            result *= numbers[i + 1]
        else:  # '||' concatenation operator
            # Convert current result and next number to strings and concatenate
            result = int(str(result) + str(numbers[i + 1]))
    return result

def can_satisfy_equation(test_value, numbers):
    """Check if any combination of operators can satisfy the equation."""
    # Generate all possible combinations of operators
    num_operators = len(numbers) - 1
    possible_operators = list(product(['+', '*', '||'], repeat=num_operators))

    # Try each combination
    for operators in possible_operators:
        try:
            if evaluate_expression(numbers, operators) == test_value:
                return True
        except (ValueError, OverflowError):
            # Skip combinations that might cause numerical errors
            continue
    return False

def solve_calibration(filename):
    """Process input file and solve the calibration puzzle."""
    total = 0

    with open(filename, 'r') as file:
        for line in file:
            # Skip empty lines
            if not line.strip():
                continue

            # Parse the line
            test_part, numbers_part = line.strip().split(':')
            test_value = int(test_part)
            numbers = [int(x) for x in numbers_part.strip().split()]

            # Check if equation can be satisfied
            if can_satisfy_equation(test_value, numbers):
                total += test_value

    return total

def main():
    result = solve_calibration("input_1.txt")
    print(f"Total calibration result: {result}")

if __name__ == "__main__":
    main()
