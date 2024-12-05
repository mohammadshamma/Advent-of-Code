# Conversation with Gemini flash: https://g.co/gemini/share/6aa01b1d4483

def is_order_correct(update, rules):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if f"{update[j]}|{update[i]}" in rules:
                return False
    return True

def sort_update(update, rules):
    sorted_update = []
    while update:
        for page in update:
            if not any(f"{page}|{other_page}" in rules for other_page in update):
                sorted_update.append(page)
                update.remove(page)
                break
    return sorted_update

def find_middle_page(update):
    return update[len(update) // 2]

def main():
    rules = set()
    with open("input_1.txt", "r") as f:
        line = f.readline().strip()
        while line:
            rules.add(line)
            line = f.readline().strip()

        updates = [list(map(int, line.strip().split(","))) for line in f]

    incorrect_updates = [update for update in updates if not is_order_correct(update, rules)]
    corrected_updates = [sort_update(update.copy(), rules) for update in incorrect_updates]
    middle_page_sum = sum(find_middle_page(update) for update in corrected_updates)

    print(middle_page_sum)

if __name__ == "__main__":
    main()
