#!/usr/bin/env python3 

import statistics


OPENERS = '([<{'


WRONG_CLOSER_TO_PENALTY = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}


COMPLETION_SCORE = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4
}


OPENER_TO_CLOSER = {
  '(': ')',
  '[': ']',
  '<': '>',
  '{': '}'
}


CLOSER_TO_OPENER = {v: k for k, v in OPENER_TO_CLOSER.items()}

COMPLETE = 'complete'
INCOMPLETE = 'incomplete'
CORRUPT = 'corrupt'


def GetLines(path):
  with open(path) as f:
    return f.readlines()


def GetLineState(line):
  stack = []
  for c in line:
    if c in OPENERS:
      stack.append(c)
    elif len(stack) and CLOSER_TO_OPENER[c] == stack[-1]:
      stack.pop()
    else:
      return CORRUPT, c
  if len(stack):
    return INCOMPLETE, stack
  return COMPLETE, None


def CalculateCorruptionScore(line):
  state, extra = GetLineState(line)
  if state == CORRUPT:
    return WRONG_CLOSER_TO_PENALTY[extra]
  return 0
  

def CalculateCompletionScore(line):
  state, extra = GetLineState(line)
  if state == INCOMPLETE:
    score = 0
    for c in reversed(extra):
      score *= 5
      score += COMPLETION_SCORE[OPENER_TO_CLOSER[c]]
    return score
  return None


def CalculateTotalCorruptionScore(path):
  lines = GetLines(path)
  return sum([CalculateCorruptionScore(line.strip()) for line in lines])


def CalculateTotalCompletionScore(path):
  lines = GetLines(path)
  scores = [CalculateCompletionScore(line.strip()) for line in lines]
  scores = filter(lambda score: score is not None, scores)
  return statistics.median(scores)


def Test():
  error_score = CalculateTotalCorruptionScore('example.txt')
  assert(error_score == 26397)
  completion_score = CalculateTotalCompletionScore('example.txt')
  assert(completion_score == 288957)


def SolvePartOne():
  error_score = CalculateTotalCorruptionScore('input.txt')
  print(f'error score = {error_score}')
  assert(error_score == 266301)


def SolvePartTwo():
  completion_score = CalculateTotalCompletionScore('input.txt')
  print(f'completion score = {completion_score}')
  assert(completion_score == 3404870164)


def Main():
  print('Hello Day 10!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()