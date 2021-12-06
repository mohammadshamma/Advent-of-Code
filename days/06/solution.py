#!/usr/bin/env python3 

from collections import defaultdict


def ReadFishAgeList(path):
  fish_age_list_str = None
  with open(path) as f:
    fish_age_list_str = f.readline().split(',')
  return [int(fish_age_str) for fish_age_str in fish_age_list_str]

def SolvePartOne():
  fish_age_list = ReadFishAgeList('input.txt')
  for day in range(80):
    for i in range(len(fish_age_list)):
      if fish_age_list[i] == 0:
        fish_age_list[i] = 6
        fish_age_list.append(8)
      else:
        fish_age_list[i] -= 1
  print(f'Number of fish after 80 days: {len(fish_age_list)}')


def Main():
  print('Hello Day 6!')
  SolvePartOne()


if __name__ == '__main__':
  Main()