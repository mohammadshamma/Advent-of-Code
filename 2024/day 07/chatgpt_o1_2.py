# Chat GPT o1 conversation: https://chatgpt.com/share/67550031-353c-800e-b267-4d9feff8c350
# Conversation steps: 1

from itertools import product

def evaluate_expression(nums, ops):
    """Evaluate the expression given nums and ops (all the same length-1).
       Operators in ops can be '+', '*', '||'.
       Evaluate strictly left-to-right."""
    # Start with the first number
    result = nums[0]
    for i, op in enumerate(ops):
        next_num = nums[i+1]
        if op == '+':
            result = result + next_num
        elif op == '*':
            result = result * next_num
        elif op == '||':
            # Concatenate: Convert to strings, then back to int
            result = int(str(result) + str(next_num))
        else:
            raise ValueError("Unknown operator encountered.")
    return result

def can_form_value(target, nums):
    """Check if we can place '+', '*', '||' between nums to get target."""
    # If only one number, check directly
    if len(nums) == 1:
        return nums[0] == target

    # Try all possible combinations of '+', '*', '||'
    for ops in product(['+', '*', '||'], repeat=len(nums)-1):
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

            # Split by ':'
            left, right = line.split(':')
            target = int(left.strip())
            nums = list(map(int, right.strip().split()))

            if can_form_value(target, nums):
                total += target

    print(total)

if __name__ == "__main__":
    main()
