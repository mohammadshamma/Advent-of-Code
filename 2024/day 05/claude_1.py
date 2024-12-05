# Conversation with Claude: https://claude.site/artifacts/b69eb4b1-8ce8-444f-b75d-e9403c70510e

def parse_input(filename):
    """
    Parse the input file into ordering rules and updates.

    Returns:
    - rules (set of tuples): Page ordering rules where each tuple (x, y)
      means x must come before y
    - updates (list of lists): List of page updates to check
    """
    with open(filename, 'r') as file:
        # Split the input into sections
        content = file.read().strip().split('\n\n')

    # Parse ordering rules
    rules = set()
    for line in content[0].split('\n'):
        if '|' in line:
            x, y = map(int, line.split('|'))
            rules.add((x, y))

    # Parse updates
    updates = [list(map(int, line.split(','))) for line in content[1].split('\n')]

    return rules, updates

def is_valid_order(update, rules):
    """
    Check if the update is in a valid order according to the rules.

    Args:
    - update (list): List of page numbers
    - rules (set): Set of page ordering rules

    Returns:
    - bool: True if update is in valid order, False otherwise
    """
    # Only consider rules where both pages are in the update
    relevant_rules = {(x, y) for (x, y) in rules if x in update and y in update}

    # Check each rule
    for x, y in relevant_rules:
        # Find indices of x and y in the update
        x_index = update.index(x)
        y_index = update.index(y)

        # If x comes after y, the order is invalid
        if x_index > y_index:
            return False

    return True

def solve_page_order_problem(filename):
    """
    Solve the page order problem by finding valid updates and their middle pages.

    Returns:
    - int: Sum of middle page numbers from valid updates
    """
    # Parse input
    rules, updates = parse_input(filename)

    # Track middle page numbers of valid updates
    middle_page_numbers = []

    # Check each update
    for update in updates:
        if is_valid_order(update, rules):
            # Find middle page (works for both odd and even lengths)
            middle_index = len(update) // 2
            middle_page_numbers.append(update[middle_index])

    # Return sum of middle page numbers
    return sum(middle_page_numbers)

# Solve the problem
result = solve_page_order_problem('input_1.txt')
print(f"Sum of middle page numbers from correctly-ordered updates: {result}")
