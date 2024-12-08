# Chat GPT o1 convesation: https://chatgpt.com/share/67550031-353c-800e-b267-4d9feff8c350
# Conversation steps: 1

from itertools import product

def evaluate_expression(nums, ops):
    """Evaluate the expression represented by nums and ops (lists),
    applying operations left-to-right (not by standard precedence).
    nums: list of integers
    ops: list of strings in {"+", "*"} with length = len(nums)-1
    """
    result = nums[0]
    for i, op in enumerate(ops):
        if op == '+':
            result = result + nums[i+1]
        else:  # op == '*'
            result = result * nums[i+1]
    return result

def can_form_value(target, nums):
    """Check if we can place '+' or '*' between nums to get target."""
    if len(nums) == 1:
        return nums[0] == target

    # Try all possible combinations of '+' and '*'
    for ops in product(['+', '*'], repeat=len(nums)-1):
        val = evaluate_expression(nums, ops)
        if val == target:
            return True
    return False

def main():
    total = 0
    with open("input_1.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Example line format:
            # 190: 10 19
            # split by ':' first
            left, right = line.split(':')
            target = int(left.strip())
            nums = list(map(int, right.strip().split()))

            if can_form_value(target, nums):
                total += target

    print(total)

if __name__ == "__main__":
    main()
