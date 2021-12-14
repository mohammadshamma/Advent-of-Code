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


def CalculateNextSequence(sequence, insertion_rules):
  new_sequence = [sequence[0]]
  for i in range(len(sequence) - 1):
    insertion = insertion_rules.get(sequence[i:i+2], '')
    new_sequence.append(insertion)
    new_sequence.append(sequence[i+1])
  return ''.join(new_sequence)


def CalculateNextNSteps(sequence, insertion_rules, n):
  for step in range(n):
    sequence = CalculateNextSequence(sequence, insertion_rules)
  return sequence


def CalculateDifferenceBetweenMostAndLeastRecurringCharacters(sequence):
  character_counters = defaultdict(lambda: 0)
  for c in sequence:
    character_counters[c] += 1
    character_counters
  max_recurrence = max(character_counters.values())
  min_recurrence = min(character_counters.values())
  return max_recurrence - min_recurrence


def CalculateDifferenceAfter10Steps(path):
  initial_sequence, insertion_rules = ReadInput(path)
  sequence = CalculateNextNSteps(initial_sequence, insertion_rules, 10)
  return CalculateDifferenceBetweenMostAndLeastRecurringCharacters(sequence)


def Test():
  difference = CalculateDifferenceAfter10Steps('example.txt')
  assert(difference == 1588)


def SolvePartOne():
  difference = CalculateDifferenceAfter10Steps('input.txt')
  print(f'Difference between most and least recurring character = {difference}')


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 13!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()