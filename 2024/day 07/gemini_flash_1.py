# Gemini flash conversation: https://g.co/gemini/share/7577a80b0b10
# Conversation steps: 8

def generate_expressions(numbers):
    if len(numbers) == 1:
        return [str(numbers[0])]

    sub_expressions = generate_expressions(numbers[1:])
    expressions = []
    for expr in sub_expressions:
        for op in ['+', '*']:
            expressions.append(f"{numbers[0]} {op} {expr}")
    return expressions

def evaluate_expression(expression):
    """Evaluates an expression with + and * operators, evaluated left-to-right."""
    tokens = expression.split()
    if len(tokens) == 1:
        return int(tokens[0])

    result = int(tokens[0])
    for i in range(1, len(tokens), 2):
        operator = tokens[i]
        operand = int(tokens[i+1])
        if operator == '+':
            result += operand
        elif operator == '*':
            result *= operand
    return result

def is_valid_equation(equation_str):
    """Checks if an equation is valid by evaluating the expression."""
    test_value, numbers = equation_str.split(': ')
    test_value = int(test_value)
    numbers = [int(num) for num in numbers.split()]

    for expression in generate_expressions(numbers):
        result = evaluate_expression(expression)
        if result is not None and result == test_value:
            return True
    return False

def main():
    with open("input_1.txt", "r") as f:
        equations = f.readlines()

    total_calibration_result = 0
    for equation in equations:
        if is_valid_equation(equation.strip()):
            test_value = int(equation.split(': ')[0])
            total_calibration_result += test_value

    print(total_calibration_result)

if __name__ == "__main__":
    main()
