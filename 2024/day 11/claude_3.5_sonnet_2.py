# Claude 3.5 Sonnet artifact: https://claude.site/artifacts/16bd2693-be87-4f66-aaa9-75c48459db33
# Conversation Steps: 7

from collections import defaultdict
from typing import Dict
import math

def count_digits(n: int) -> int:
    return len(str(n))

def split_number(n: int) -> tuple[int, int]:
    str_n = str(n)
    mid = len(str_n) // 2
    return int(str_n[:mid]), int(str_n[mid:])

class StoneCounter:
    def __init__(self):
        self.memo = {}

    def evolve_count(self, number: int, count: int, blinks: int) -> Dict[int, int]:
        """
        Calculate how many stones a specific number will produce after n blinks
        Returns a dictionary mapping resulting numbers to their counts
        """
        # Check memo
        memo_key = (number, blinks)
        if memo_key in self.memo:
            result = defaultdict(int)
            for num, cnt in self.memo[memo_key].items():
                result[num] = cnt * count
            return result

        # Base case
        if blinks == 0:
            return {number: count}

        result = defaultdict(int)

        # Apply transformation rules
        if number == 0:
            # Evolve all zeros to ones
            sub_result = self.evolve_count(1, count, blinks - 1)
            for num, cnt in sub_result.items():
                result[num] += cnt
        else:
            digit_count = count_digits(number)
            if digit_count % 2 == 0:
                # Split numbers
                left, right = split_number(number)
                left_result = self.evolve_count(left, count, blinks - 1)
                right_result = self.evolve_count(right, count, blinks - 1)
                for num, cnt in left_result.items():
                    result[num] += cnt
                for num, cnt in right_result.items():
                    result[num] += cnt
            else:
                # Multiply by 2024
                new_num = number * 2024
                sub_result = self.evolve_count(new_num, count, blinks - 1)
                for num, cnt in sub_result.items():
                    result[num] += cnt

        # Memoize the result for a single count
        self.memo[memo_key] = {num: cnt // count for num, cnt in result.items()}
        return result

def solve_stone_puzzle(filename: str, blinks: int = 75) -> int:
    # Read initial stones
    with open(filename) as f:
        numbers = [int(x) for x in f.read().strip().split()]

    # Count initial frequencies
    number_counts = defaultdict(int)
    for num in numbers:
        number_counts[num] += 1

    # Simulate evolution
    counter = StoneCounter()
    current_step = 0

    while current_step < blinks:
        new_counts = defaultdict(int)

        # Process each unique number and its count
        for number, count in number_counts.items():
            evolved = counter.evolve_count(number, count, 1)
            for num, cnt in evolved.items():
                new_counts[num] += cnt

        number_counts = new_counts
        current_step += 1

        if current_step % 5 == 0:
            total = sum(number_counts.values())
            print(f"Step {current_step}: {total:,} stones "
                  f"({len(number_counts)} unique numbers)")

    return sum(number_counts.values())

if __name__ == "__main__":
    result = solve_stone_puzzle("input_1.txt")
    print(f"\nFinal result: {result:,} stones")
