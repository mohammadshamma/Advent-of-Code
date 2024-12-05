# Conversation with Gemini: https://g.co/gemini/share/1fba03bbc76d

from collections import defaultdict


def is_valid_order(order, rules):
    """
    Checks if a given page order is valid according to the rules.

    Args:
      order: A list of page numbers in the order they are to be printed.
      rules: A dictionary of ordering rules, where keys are page numbers
             and values are sets of page numbers that must come after the key.

    Returns:
      True if the order is valid, False otherwise.
    """
    for rule_x, rule_ys in rules.items():
        if rule_x in order:
            for rule_y in rule_ys:
                if rule_y in order and order.index(rule_x) > order.index(rule_y):
                    return False
    return True


def get_middle_page(order):
    """
    Calculates the middle page number of a given order.

    Args:
      order: A list of page numbers.

    Returns:
      The middle page number.
    """
    if not order:  # Handle empty order
        return 0  # Or any appropriate default value
    middle_index = len(order) // 2
    if len(order) % 2 == 0:  # Even number of pages
        return (order[middle_index - 1] + order[middle_index]) // 2
    else:  # Odd number of pages
        return order[middle_index]


def topological_sort(update, rules):
    """
    Performs topological sort to order the pages in an update according to the rules.

    Args:
      update: A list of page numbers in an update.
      rules: A dictionary of ordering rules.

    Returns:
      A list of page numbers in the correct order.
    """
    graph = defaultdict(list)
    in_degree = {}
    for x, ys in rules.items():
        for y in ys:
            if x in update and y in update:  # Only consider rules for pages in the update
                graph[x].append(y)
                in_degree[y] = in_degree.get(y, 0) + 1
    for page in update:
        if page not in in_degree:
            in_degree[page] = 0
    queue = [page for page in update if in_degree[page] == 0]
    result = []
    while queue:
        curr = queue.pop(0)
        result.append(curr)
        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result  # Return only the reordered pages


def main():
    """
    Reads input from file, processes updates, and calculates the sum of middle pages.
    """
    rules = {}
    updates = []
    with open("input_1.txt", "r") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                # Process rule
                x, y = map(int, line.split("|"))
                rules.setdefault(x, set()).add(y)
            elif line:
                # Process update
                updates.append(list(map(int, line.split(","))))

    invalid_updates = [update for update in updates if not is_valid_order(update, rules)]

    # Correctly order the invalid updates
    ordered_updates = [topological_sort(update, rules) for update in invalid_updates]

    middle_pages_sum = sum(get_middle_page(update) for update in ordered_updates)

    print(f"Ordered invalid updates: {ordered_updates}")
    print(f"Sum of middle page numbers from correctly-ordered invalid updates: {middle_pages_sum}")


if __name__ == "__main__":
    main()
