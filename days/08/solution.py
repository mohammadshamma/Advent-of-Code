#!/usr/bin/env python3 

from collections import defaultdict

# Some notes and running through an example:
#
# 0: abcefg  len = 6
# 1: cf      len = 2*
# 2: acdeg   len = 5
# 3: acdfg   len = 5
# 4: bcdf    len = 4*
# 5: abdfg   len = 5
# 6: abdefg  len = 6
# 7: acf     len = 3*
# 8: abcdefg len = 7*
# 9: abcdfg  len = 6
#
# Example acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
# ab => 1: (a, b) -> (c, f)
# dab => 7: (d, a, b) -> (a, c, f)
# eafb => 4: (e, a, f, b) -> (b, c, d, f)
# cdfbe gcdfa fbcad => 2, 3, 5: acdeg, acdfg, abdfg.
#   r1: (e, g) -> (e, b)
#   r2: (b, a) -> (c, f)
#   r3: (c, d, f) -> (a, d, g)
# cefabd cdfgeb cagedb => 0, 6, 9: abcefg, abdefg, abcdfg
#   r1: () -> ()
#   r2: (f, a, g) -> (c, e, d)
#   r3: (c, e, b, d) -> (a, b, f, g)
#
# So given the 1 and the 7, we can infer what maps to segment A.
# 
# Wire\Segment  A  B  C  D  E  F  G
#      A        X  X  O  X  X  X  X
#      B        X  X  X  X  X  O  X
#      C        X  X  X  X  X  X  O 
#      D        O  X  X  X  X  X  X
#      E        X  O  X  X  X  X  X
#      F        X  X  X  O  X  X  X
#      G        X  X  X  X  O  X  X
#
# cdfeb => gadbf => abdgf => 5
# fcadb => dgcaf => acdgf => 3
# cdfeb => gadbf => abdgf => 5
# cdbaf => gafcd => acdgf => 3
#
# Result 5353

SEGMENT_COUNT = 7

SEGMENT_COMBINATIONS = {
  0: 'abcefg',
  1: 'cf',
  2: 'acdeg',
  3: 'acdfg',
  4: 'bcdf',
  5: 'abdfg',
  6: 'abdefg',
  7: 'acf',
  8: 'abcdefg',
  9: 'abcdfg',
}

COMBINATION_TO_NUMBER = {v: k for k, v in SEGMENT_COMBINATIONS.items()}

def ctoi(character):
  return ord(character) - ord('a')

def itoc(integer):
  return chr(integer + ord('a'))

class SignalToSegmentMappingConstraintManager(object):

  def __init__(self):
    self.signal_constraints = [['?' for i in range(SEGMENT_COUNT)] for i in range(SEGMENT_COUNT)]

  def __str__(self):
    str =  '             Segment   \n'
    str += 'Signal    a b c d e f g\n'
    for i in range(SEGMENT_COUNT):
      str += '  %s       %s\n' % (itoc(i), " ".join(self.signal_constraints[i]))
    return str

  def SetConstraint(self, signal, segments):
    signal_index = ctoi(signal)
    segment_indices = [ctoi(segment) for segment in segments]
    last_open_possibility_index = None
    open_possibilites_count = 0
    for segment_index in range(SEGMENT_COUNT):
      if segment_index not in segment_indices:
        self.signal_constraints[signal_index][segment_index] = 'x'
      else:
        if self.signal_constraints[signal_index][segment_index] == '?':
          last_open_possibility_index = segment_index
          open_possibilites_count += 1
    if open_possibilites_count == 1:
      self.signal_constraints[signal_index][last_open_possibility_index] = 'o'

  def GetSignalToSegmentMap(self):
    self._CheckAndFillForegoneConclusions()
    signal_to_segment_map = {}
    for i in range(SEGMENT_COUNT):
      signal_to_segment_map[itoc(i)] = itoc(self.signal_constraints[i].index('o'))
    return signal_to_segment_map

  def _CheckAndFillForegoneConclusions(self):
    updated_constraints_matrix = False
    while True:
      for signal_index in range(SEGMENT_COUNT):
        # Check row for six rejections and an open slot, and fill in conclusion.
        rejection_count = sum([1 if self.signal_constraints[signal_index][i] == 'x' else 0 for i in range(SEGMENT_COUNT)])
        has_open_slot = '?' in self.signal_constraints[signal_index]
        if rejection_count == 6 and has_open_slot:
          open_slot_index = self.signal_constraints[signal_index].index('?')
          self.signal_constraints[signal_index][open_slot_index] = 'o'
          updated_constraints_matrix = True
        # Check row for conclusion and reject open slots.
        has_conclusion = 'o' in self.signal_constraints[signal_index]
        has_open_slot = '?' in self.signal_constraints[signal_index]
        if has_conclusion and has_open_slot:
          for segment_index in range(SEGMENT_COUNT):
            if self.signal_constraints[signal_index][segment_index] == '?':
              self.signal_constraints[signal_index][segment_index] = 'x'
              updated_constraints_matrix = True

      for segment_index in range(SEGMENT_COUNT):
        # Check column for six rejections and an open slot, and fill in conclusion.
        rejection_count = sum([1 if self.signal_constraints[i][segment_index] == 'x' else 0 for i in range(SEGMENT_COUNT)])
        has_open_slot = '?' in [self.signal_constraints[i][segment_index] for i in range(SEGMENT_COUNT)]
        if rejection_count == 6 and has_open_slot:
          open_slot_index = [self.signal_constraints[i][segment_index] for i in range(SEGMENT_COUNT)].index('?')
          self.signal_constraints[open_slot_index][segment_index] = 'o'
          updated_constraints_matrix = True
        # Check column for conclusion and reject open slots.
        has_conclusion = 'o' in [self.signal_constraints[i][segment_index] for i in range(SEGMENT_COUNT)]
        has_open_slot = '?' in [self.signal_constraints[i][segment_index] for i in range(SEGMENT_COUNT)]
        if has_conclusion and has_open_slot:
          for signal_index in range(SEGMENT_COUNT):
            if self.signal_constraints[signal_index][segment_index] == '?':
              self.signal_constraints[signal_index][segment_index] = 'x'
              updated_constraints_matrix = True

      if not updated_constraints_matrix:
        break
      updated_constraints_matrix = False
    

def GetObservedEntries(path):
  with open(path) as f:
    entries = []
    for line in f.readlines():
      tokens = line.split('|')
      assert(len(tokens) == 2)
      combinations = tokens[0].strip().split()
      four_digits = tokens[1].strip().split()
      entries.append((combinations, four_digits))
    return entries


def BucketStringsBySize(strs):
  buckets = defaultdict(list)
  for str in strs:
    buckets[len(str)].append(str)
  return buckets


def DeconstructCombinationsBasedOnRecurrence(combinations):
  all_characters = set(''.join(combinations))
  recurrence_to_characters = defaultdict(list)
  for character in all_characters:
    character_recurrence = 0
    for combination in combinations:
      if character in combination:
        character_recurrence += 1
    recurrence_to_characters[character_recurrence].append(character)
  return {recurrence: ''.join(characters) for recurrence, characters in recurrence_to_characters.items()}    


def GetConstraints(observed_combinations):
  bucketed_valid_combinations = BucketStringsBySize(SEGMENT_COMBINATIONS.values())
  bucketed_observed_combinations = BucketStringsBySize(observed_combinations)
  assert(len(bucketed_valid_combinations) == len(bucketed_observed_combinations))
  constraints = []
  for size in bucketed_valid_combinations.keys():
    assert(len(bucketed_valid_combinations[size]) == len(bucketed_observed_combinations[size]))
    if size == 1:
      constraints.append((bucketed_observed_combinations[size][0], bucketed_valid_combinations[size][0]))
    else:
      # Deconstruct the combinations based on signal/segment recurrence.
      valid_recurrence_groups = DeconstructCombinationsBasedOnRecurrence(bucketed_valid_combinations[size])
      observed_recurrence_groups = DeconstructCombinationsBasedOnRecurrence(bucketed_observed_combinations[size])
      assert(len(valid_recurrence_groups) == len(observed_recurrence_groups))
      for recurrence in valid_recurrence_groups.keys():
        assert(recurrence in observed_recurrence_groups)
        constraints.append((observed_recurrence_groups[recurrence], valid_recurrence_groups[recurrence]))
  return constraints


def GetSignalToSegmentMap(observed_combinations):
  constraints = GetConstraints(observed_combinations)
  constraint_manager = SignalToSegmentMappingConstraintManager()
  for contraint in constraints:
    for signal in contraint[0]:
     segments = contraint[1]
     constraint_manager.SetConstraint(signal, segments)
  return constraint_manager.GetSignalToSegmentMap()


def CalculateDisplayValue(signal_to_segment_map, segment):
  translated_segment = ''.join(sorted([signal_to_segment_map[char] for char in segment]))
  return COMBINATION_TO_NUMBER[translated_segment]


def CalculateAllDisplaysValue(signal_to_segment_map, displays_segments):
  value = 0
  for segment in displays_segments:
    value *= 10
    value += CalculateDisplayValue(signal_to_segment_map, segment)
  return value


def Solve(input_path):
  observed_entries = GetObservedEntries(input_path)
  sum_of_all_display_values = 0
  for observed_entry in observed_entries:
    observed_combinations = observed_entry[0]
    displays_segments = observed_entry[1]
    signal_to_segment_map = GetSignalToSegmentMap(observed_combinations)
    display_value = CalculateAllDisplaysValue(signal_to_segment_map, displays_segments)
    sum_of_all_display_values += display_value
  return sum_of_all_display_values


def TestConstraintExtraction():
  _ = GetConstraints(['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'])


def TestConstraintEngine():
  constraint_tuples = [
    ('ab', 'cf'),
    ('dab', 'acf'),
    ('eafb', 'bcdf'),
    ('eg', 'eb'),
    ('ba', 'cf'),
    ('cdf', 'adg'),
    ('fag', 'ced'),
    ('cebd', 'abfg'),
  ]
  cm = SignalToSegmentMappingConstraintManager()
  for contraint_tuple in constraint_tuples:
    for signal in contraint_tuple[0]:
     segments = contraint_tuple[1]
     cm.SetConstraint(signal, segments)
  assert(cm.GetSignalToSegmentMap() == {'a': 'c', 'b': 'f', 'c': 'g', 'd': 'a', 'e': 'b', 'f': 'd', 'g': 'e'})


def TestExample():
  observed_combinations = ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab']
  displays_segments = ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']
  signal_to_segment_map = GetSignalToSegmentMap(observed_combinations)
  display_value = CalculateAllDisplaysValue(signal_to_segment_map, displays_segments)
  assert(display_value == 5353)


def Test():
  TestConstraintExtraction()
  TestConstraintEngine()
  TestExample()


def SolvePart1():
  observed_entries = GetObservedEntries('input.txt')
  unique_segment_count_occurences = sum([sum([1 if len(segment) in (2,3,4,7) else 0 for segment in entry[1]]) for entry in observed_entries])
  print(f'1, 4, 7 and 8 appear: {unique_segment_count_occurences}')


def SolvePart2():
  sum_of_displays = Solve('input.txt')
  assert(sum_of_displays == 990964)
  print(f'Sum of all displays = {sum_of_displays}')


# def BigBoy():
#   sum_of_displays = Solve('8-100000.in')
#   assert(sum_of_displays == 498570828)
#   print(f'Sum of all displays = {sum_of_displays}')


def Main():
  print('Hello Day 8!')
  Test()
  SolvePart1()
  SolvePart2()
  # To run the BigBoys(), download the big input from: https://the-tk.com/files/aoc2021-bigboys/8-100000.in.xz
  # BigBoy()


if __name__ == '__main__':
  Main()
