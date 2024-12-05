# Conversation with ChatGPT: https://chatgpt.com/share/6751427b-61f4-800e-825c-73f516285415

from collections import defaultdict

def parse_input(file_path):
    """Parse the input file into rules and updates."""
    with open(file_path, 'r') as f:
        lines = f.read().strip().split("\n")

    # Split into two sections: rules and updates
    rules_section, updates_section = "\n".join(lines).split("\n\n")

    # Parse rules
    rules = []
    for rule in rules_section.splitlines():
        x, y = map(int, rule.split('|'))
        rules.append((x, y))

    # Parse updates
    updates = []
    for update in updates_section.splitlines():
        updates.append(list(map(int, update.split(','))))

    return rules, updates

def is_correct_order(update, rules):
    """Check if the update respects the given rules."""
    # Create a map of positions for the pages in the update
    positions = {page: idx for idx, page in enumerate(update)}

    for x, y in rules:
        # Only consider the rule if both pages are in the update
        if x in positions and y in positions:
            # Check if x comes before y
            if positions[x] >= positions[y]:
                return False
    return True

def main():
    # Parse input
    rules, updates = parse_input("input_1.txt")

    total_middle_sum = 0

    for update in updates:
        if is_correct_order(update, rules):
            # Find the middle page number
            middle_page = update[len(update) // 2]
            total_middle_sum += middle_page

    print("Sum of middle page numbers from correctly-ordered updates:", total_middle_sum)

if __name__ == "__main__":
    main()
