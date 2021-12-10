#!/usr/bin/env python3 

OPENERS = '([<{'


WRONG_CLOSER_TO_PENALTY = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}


OPENER_TO_CLOSER = {
  '(': ')',
  '[': ']',
  '<': '>',
  '{': '}'
}


CLOSER_TO_OPENER = {v: k for k, v in OPENER_TO_CLOSER.items()}


def GetLines(path):
  with open(path) as f:
    return f.readlines()


def CalculateCorruptionScore(line):
  stack = []
  for c in line:
    if c in OPENERS:
      stack.append(c)
    elif len(stack) and CLOSER_TO_OPENER[c] == stack[-1]:
      stack.pop()
    else:
      return WRONG_CLOSER_TO_PENALTY[c]
  return 0


def CalculateTotalCorruptionScore(path):
  lines = GetLines(path)
  return sum([CalculateCorruptionScore(line.strip()) for line in lines])


def Test():
  error_score = CalculateTotalCorruptionScore('example.txt')
  assert(error_score == 26397)


def SolvePartOne():
  error_score = CalculateTotalCorruptionScore('input.txt')
  print(f'error score = {error_score}')
  assert(error_score == 266301)


def Main():
  print('Hello Day 10!')
  Test()
  SolvePartOne()


if __name__ == '__main__':
  Main()