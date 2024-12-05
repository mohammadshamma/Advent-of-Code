# Conversation with ChatGPT: https://chatgpt.com/share/6751427b-61f4-800e-825c-73f516285415

from collections import defaultdict, deque

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

def fix_order(update, rules):
    """Fix the order of pages in the update according to the rules."""
    # Build a graph of dependencies
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    pages = set(update)

    for x, y in rules:
        if x in pages and y in pages:
            graph[x].append(y)
            in_degree[y] += 1
            in_degree.setdefault(x, 0)

    # Perform topological sort to determine the correct order
    queue = deque([node for node in pages if in_degree[node] == 0])
    sorted_update = []

    while queue:
        current = queue.popleft()
        sorted_update.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update

def main():
    # Parse input
    rules, updates = parse_input("input_1.txt")

    incorrect_updates = []
    total_middle_sum = 0

    for update in updates:
        if not is_correct_order(update, rules):
            # Fix the order of the update
            corrected_update = fix_order(update, rules)
            incorrect_updates.append(corrected_update)
            # Find the middle page number
            middle_page = corrected_update[len(corrected_update) // 2]
            total_middle_sum += middle_page

    print("Sum of middle page numbers from fixed incorrectly-ordered updates:", total_middle_sum)

if __name__ == "__main__":
    main()
