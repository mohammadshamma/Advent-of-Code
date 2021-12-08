#!/usr/bin/env python3 

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


def GetObservedEntries(path):
  with open(path) as f:
    entries = []
    for line in f.readlines():
      tokens = line.split('|')
      assert(len(tokens) == 2)
      signals = tokens[0].strip().split()
      segments = tokens[1].strip().split()
      entries.append((signals, segments))
    return entries


def SolvePart1():
  observed_entries = GetObservedEntries('input.txt')
  unique_segment_count_occurences = sum([sum([1 if len(segment) in (2,3,4,7) else 0 for segment in entry[1]]) for entry in observed_entries])
  print(f'1, 4, 7 and 8 appear: {unique_segment_count_occurences}')


def Main():
  print('Hello Day 8!')
  SolvePart1()


if __name__ == '__main__':
  Main()