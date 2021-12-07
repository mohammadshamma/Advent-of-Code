#!/usr/bin/env python3 

from collections import defaultdict


class RingIntegerList():
  def __init__(self, size):
    self.list = [0] * size
    self.offset = 0

  def ShiftLeft(self):
    self.offset += 1
    if(self.offset >= len(self.list)):
      self.offset = 0

  def _GetRealIndex(self, index, offset):
    return (index + offset) % len(self.list)

  def GetValue(self, index):
    real_index = self._GetRealIndex(index, self.offset)
    return self.list[real_index]

  def BumpValue(self, index, value):
    real_index = self._GetRealIndex(index, self.offset)
    self.list[real_index] += value


def ReadFishAgeList(path):
  fish_age_list_str = None
  with open(path) as f:
    fish_age_list_str = f.readline().split(',')
  return [int(fish_age_str) for fish_age_str in fish_age_list_str]


def CalculateFishCountAfterNDays(day_count, fish_age_list):
  fish_age_buckets = RingIntegerList(9)
  for fish_age in fish_age_list:
    fish_age_buckets.BumpValue(fish_age, 1)
  for day in range(day_count):
    zero_fishes = fish_age_buckets.GetValue(0)
    fish_age_buckets.ShiftLeft()
    fish_age_buckets.BumpValue(6, zero_fishes)
  return sum(fish_age_buckets.list)


def SolvePartOne():
  fish_age_list = ReadFishAgeList('input.txt')
  fish_count = CalculateFishCountAfterNDays(80, fish_age_list)
  assert(fish_count == 379414)
  print(f'Number of fish after 80 days: {fish_count}')


def SolvePartTwo():
  fish_age_list = ReadFishAgeList('input.txt')
  fish_count = CalculateFishCountAfterNDays(256, fish_age_list)
  assert(fish_count == 1705008653296)
  print(f'Number of fish after 256 days: {fish_count}')


def BigBoy():
  fish_count = CalculateFishCountAfterNDays(9999999, [3,4,3,1,2])
  print(f'Number of fish after 256 days: {fish_count}')


def Main():
  print('Hello Day 6!')
  SolvePartOne()
  SolvePartTwo()
  BigBoy()


if __name__ == '__main__':
  Main()