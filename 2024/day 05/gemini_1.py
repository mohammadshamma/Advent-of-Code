# Conversation wit Gemini: https://g.co/gemini/share/a7d061854f0e

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
    middle_index = len(order) // 2
    return order[middle_index]


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

    valid_updates = [update for update in updates if is_valid_order(update, rules)]

    middle_pages_sum = sum(get_middle_page(update) for update in valid_updates)

    print(f"Sum of middle page numbers from correctly-ordered updates: {middle_pages_sum}")


if __name__ == "__main__":
    main()
