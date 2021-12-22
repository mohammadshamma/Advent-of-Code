#!/usr/bin/env python3 

import numpy as np


def GetRange(range_str, prefix):
  assert(range_str.startswith(prefix))
  x_range = range_str[len(prefix):]
  x_range = [int(number_str) for number_str in x_range.split('..')]
  assert(len(x_range) == 2)
  range_start = min(x_range)
  range_end = max(x_range)
  return range_start, range_end


def ReadRebootSequence(path):
  instructions = []
  with open(path) as f:
    for line in f.readlines():
      line = line.strip()
      parts = line.split()
      assert(len(parts) == 2)
      assert(parts[0] == 'on' or parts[0] == 'off')
      value = 1 if parts[0] == 'on' else 0
      ranges = parts[1].split(',')
      assert(len(ranges) == 3)
      x_range = GetRange(ranges[0], 'x=')
      y_range = GetRange(ranges[1], 'y=')
      z_range = GetRange(ranges[2], 'z=')
      instructions.append((value, (x_range, y_range, z_range)))
    return instructions


class Reactor(object):
  
  def __init__(self, max_coordinate_index=50, min_coordinate_index=-50):
    self.max_coordinate = max_coordinate_index
    self.min_coordinate = min_coordinate_index
    side_length = max_coordinate_index - min_coordinate_index + 1
    self.array = np.zeros((side_length, side_length, side_length))
    self.coordinate_shift = 0 - min_coordinate_index
    self.max_coordinate = side_length - 1

  def Set(self, value, cuboid_ranges):
    trimmed_cuboid_ranges = []
    for range in cuboid_ranges:
      if range[0] < self.min_coordinate or range[1] > self.max_coordinate:
        return
      trimmed_range = (max(self.min_coordinate, range[0]), min(self.max_coordinate, range[1]))
      trimmed_cuboid_ranges.append(trimmed_range)
    adjusted_ranges = [(trimmed_range[0] + self.coordinate_shift, trimmed_range[1] + self.coordinate_shift) for trimmed_range in trimmed_cuboid_ranges]
    self.array[adjusted_ranges[0][0]:adjusted_ranges[0][1]+1, adjusted_ranges[1][0]:adjusted_ranges[1][1]+1, adjusted_ranges[2][0]:adjusted_ranges[2][1]+1] = value

  def GetTurnedOnCubesCount(self):
    return np.count_nonzero(self.array == 1)


def RestartReactorAndGetTurnedOnCubesCount(reboot_sequence):
  r = Reactor()
  for v, ranges in reboot_sequence:
    r.Set(v, ranges)
  return r.GetTurnedOnCubesCount()


def Test():
  instructions = ReadRebootSequence('example.txt')
  assert(RestartReactorAndGetTurnedOnCubesCount(instructions) == 590784)



def SolvePartOne():
  turned_on_count = RestartReactorAndGetTurnedOnCubesCount(ReadRebootSequence('input.txt'))
  print(f'Part 1: Number of turned on cubes after restart = {turned_on_count}')
  assert(turned_on_count == 503864)


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 22!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()