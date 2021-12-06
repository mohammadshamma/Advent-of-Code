#!/usr/bin/env python3 

from collections import defaultdict


def ReadFishAgeList(path):
  fish_age_list_str = None
  with open(path) as f:
    fish_age_list_str = f.readline().split(',')
  return [int(fish_age_str) for fish_age_str in fish_age_list_str]


def CalculateFishCountAfterNDays(day_count):
  fish_age_list = ReadFishAgeList('input.txt')
  fish_age_buckets = [0] * 9
  for fish_age in fish_age_list:
    fish_age_buckets[fish_age] += 1
  for day in range(day_count):
    new_fish_age_buckets = [0] * 9
    # Process zero days remaining in cycle.
    new_fish_age_buckets[8] += fish_age_buckets[0]
    new_fish_age_buckets[6] += fish_age_buckets[0]
    # Process non-zero days.
    for day in range(1, 9):
      new_fish_age_buckets[day - 1] += fish_age_buckets[day]
    fish_age_buckets = new_fish_age_buckets
  return sum(fish_age_buckets)


def SolvePartOne():
  fish_age_list = ReadFishAgeList('input.txt')
  fish_count = CalculateFishCountAfterNDays(80)
  assert(fish_count == 379414)
  print(f'Number of fish after 80 days: {fish_count}')


def SolvePartTwo():
  fish_age_list = ReadFishAgeList('input.txt')
  fish_count = CalculateFishCountAfterNDays(256)
  assert(fish_count == 1705008653296)
  print(f'Number of fish after 256 days: {fish_count}')


def Main():
  print('Hello Day 6!')
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()