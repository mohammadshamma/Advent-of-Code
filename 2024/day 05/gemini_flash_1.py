# Conversation with Gemini 1.5 flash: https://g.co/gemini/share/665f83770449

def is_order_correct(update, rules):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if f"{update[j]}|{update[i]}" in rules:
                return False
    return True

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

    correct_updates = [update for update in updates if is_order_correct(update, rules)]
    middle_page_sum = sum(find_middle_page(update) for update in correct_updates)

    print(middle_page_sum)

if __name__ == "__main__":
    main()
