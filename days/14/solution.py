#!/usr/bin/env python3 


from collections import defaultdict


def ReadInput(path):
  with open(path) as f:
    initial_sequence = f.readline().strip()
    empty_line = f.readline().strip()
    assert(empty_line == '')

    insertion_rules = []
    while True:
      l = f.readline().strip()
      if not l:
        break
      parts = [part for part in l.split('->')]
      assert(len(parts) == 2)
      insertion_rules.append((parts[0].strip(), parts[1].strip()))
    
    return initial_sequence, {rule[0]: rule[1] for rule in insertion_rules}


class PolymerCalculator(object):

  def __init__(self, insertion_rules):
    self._insertion_rules = insertion_rules
    self._character_count_memoization = {}

  def AddCountersToAccumulator(accumulator, counters):
    for k, v in counters.items():
      accumulator[k] += v

  def CalculateCharacterCountForCharacterTupleAtLevelN(self, tuple, steps_ahead):
    character_count = self._character_count_memoization.get((tuple, steps_ahead), None)
    if character_count:
      return character_count
    character_count = defaultdict(lambda: 0)
    if steps_ahead == 0:
      character_count[tuple[0]] += 1
    else:
      inserted_char = self._insertion_rules[tuple]
      left_tuple = tuple[0] + inserted_char
      right_tuple = inserted_char + tuple[1]
      left_character_count = self.CalculateCharacterCountForCharacterTupleAtLevelN(left_tuple, steps_ahead - 1)
      PolymerCalculator.AddCountersToAccumulator(character_count, left_character_count)
      right_character_count = self.CalculateCharacterCountForCharacterTupleAtLevelN(right_tuple, steps_ahead - 1)
      PolymerCalculator.AddCountersToAccumulator(character_count, right_character_count)
    self._character_count_memoization[(tuple, steps_ahead)] = character_count
    return character_count

  def CalculateCharacterCountersForSequence(self, sequence, steps):
    character_count = defaultdict(lambda: 0)
    for i in range(len(sequence) - 1):
      current_character_count = self.CalculateCharacterCountForCharacterTupleAtLevelN(sequence[i: i + 2], steps)
      PolymerCalculator.AddCountersToAccumulator(character_count, current_character_count)
    character_count[sequence[-1]] += 1
    return character_count


def CalculateDifferenceAfterNStepsV2(path, step_count):
  sequence, insertion_rules = ReadInput(path)
  calculator = PolymerCalculator(insertion_rules)
  character_count = calculator.CalculateCharacterCountersForSequence(sequence, step_count)
  max_recurrence = max(character_count.values())
  min_recurrence = min(character_count.values())
  return max_recurrence - min_recurrence


def Test():
  difference = CalculateDifferenceAfterNStepsV2('example.txt', 10)
  print(difference)
  assert(difference == 1588)
  difference = CalculateDifferenceAfterNStepsV2('example.txt', 40)
  assert(difference == 2188189693529)


def SolvePartOne():
  difference = CalculateDifferenceAfterNStepsV2('input.txt', 10)
  print(f'Difference between most and least recurring character after 10 steps = {difference}')
  assert(difference == 2988)


def SolvePartTwo():
  difference = CalculateDifferenceAfterNStepsV2('input.txt', 40)
  print(f'Difference between most and least recurring character after 40 steps = {difference}')
  assert(difference == 3572761917024)


def Main():
  print('Hello Day 13!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()