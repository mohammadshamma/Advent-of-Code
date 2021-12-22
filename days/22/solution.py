#!/usr/bin/env python3 

import numpy as np
import math


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
  
  def __init__(self, max_coordinate=50, min_coordinate=-50):
    self.max_coordinate = max_coordinate
    self.min_coordinate = min_coordinate
    side_length = max_coordinate - min_coordinate + 1
    self.array = np.zeros((side_length, side_length, side_length))
    self.coordinate_shift = 0 - min_coordinate
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


class Cuboid(object):

  def __init__(self, range):
    self.range = range

  def Contains(self, other):
    if (self.range[0][0] <= other.range[0][0] and self.range[0][1] >= other.range[0][1]
     and self.range[1][0] <= other.range[1][0] and self.range[1][1] >= other.range[1][1]
     and self.range[2][0] <= other.range[2][0] and self.range[2][1] >= other.range[2][1]):
      return True
    return False

  def DoesIntersect(self, other):
    if (self.range[0][0] > other.range[0][1] or self.range[0][1] < other.range[0][0]
     or self.range[1][0] > other.range[1][1] or self.range[1][1] < other.range[1][0]
     or self.range[2][0] > other.range[2][1] or self.range[2][1] < other.range[2][0]):
      return False
    return True
  
  def __sub__(self, other):
    if not self.DoesIntersect(other):
      return [Cuboid(self.range)]

    remainder = self.range
    result = []

    # Slice resulting fragment(s) along the x axis.
    if remainder[0][1] >= other.range[0][0] and remainder[0][0] <= other.range[0][0]:
      if other.range[0][0] > remainder[0][0]:
        result.append(((remainder[0][0], other.range[0][0] - 1), remainder[1], remainder[2]))
      remainder = ((other.range[0][0], remainder[0][1]), remainder[1], remainder[2])
    if remainder[0][0] <= other.range[0][1] and remainder[0][1] >= other.range[0][1]:
      if other.range[0][1] < remainder[0][1]:
        result.append(((other.range[0][1] + 1, remainder[0][1]), remainder[1], remainder[2]))
      remainder = ((remainder[0][0], other.range[0][1]), remainder[1], remainder[2])

    # Slice resulting fragment(s) along the y axis.
    if remainder[1][1] >= other.range[1][0] and remainder[1][0] <= other.range[1][0]:
      if other.range[1][0] > remainder[1][0]:
        result.append((remainder[0], (remainder[1][0], other.range[1][0] - 1), remainder[2]))
      remainder = (remainder[0], (other.range[1][0], remainder[1][1]), remainder[2])
    if remainder[1][0] <= other.range[1][1] and remainder[1][1] >= other.range[1][1]:
      if other.range[1][1] < remainder[1][1]:
        result.append((remainder[0], (other.range[1][1] + 1, remainder[1][1]), remainder[2]))
      remainder = (remainder[0], (remainder[1][0], other.range[1][1]), remainder[2])

    # Slice resulting fragment(s) along the z axis.
    if remainder[2][1] >= other.range[2][0] and remainder[2][0] <= other.range[2][0]:
      if other.range[2][0] > remainder[2][0]:
        result.append((remainder[0], remainder[1], (remainder[2][0], other.range[2][0] - 1)))
      remainder = (remainder[0], remainder[1], (other.range[2][0], remainder[2][1]))
    if remainder[2][0] <= other.range[2][1] and remainder[2][1] >= other.range[2][1]:
      if other.range[2][1] < remainder[2][1]:
        result.append((remainder[0], remainder[1], (other.range[2][1] + 1, remainder[2][1])))
      remainder = (remainder[0], remainder[1], (remainder[2][0], other.range[2][1]))

    return [Cuboid(range) for range in result]

  def __str__(self):
    return str(self.range)

  def __repr__(self):
    return str(self.range)

  def GetSize(self):
    return math.prod([self.range[i][1] - self.range[i][0] + 1 for i in range(3)])


class ReactorV2(object):

  def __init__(self):
    self.ones_cuboids = []

  def Set(self, value, cuboid):
    if value == 1:
      new_ones_cuboids = [cuboid]
      for ones_cuboid in self.ones_cuboids:
        if cuboid.Contains(ones_cuboid):
          pass
        elif cuboid.DoesIntersect(ones_cuboid):
          new_ones_cuboids.extend(ones_cuboid - cuboid)
        else:
          new_ones_cuboids.append(ones_cuboid)
      self.ones_cuboids = new_ones_cuboids
    elif value == 0:
      new_ones_cuboids = []
      for ones_cuboid in self.ones_cuboids:
        if ones_cuboid.DoesIntersect(cuboid):
          new_ones_cuboids.extend(ones_cuboid - cuboid)
        else:
          new_ones_cuboids.append(ones_cuboid)
      self.ones_cuboids = new_ones_cuboids
    else:
      raise Exception(f'Anyhow, value {value} was not expected.')
  
  def GetTurnedOnCubesCount(self):
    return sum([c.GetSize() for c in self.ones_cuboids])
          

def RestartReactorAndGetTurnedOnCubesCount(reboot_sequence):
  r = Reactor()
  for v, ranges in reboot_sequence:
    r.Set(v, ranges)
  return r.GetTurnedOnCubesCount()


def RestartReactorAndGetTurnedOnCubesCountV2(reboot_sequence):
  r = ReactorV2()
  for v, ranges in reboot_sequence:
    r.Set(v, Cuboid(ranges))
  return r.GetTurnedOnCubesCount()


def Test():
  instructions = ReadRebootSequence('example.txt')
  assert(RestartReactorAndGetTurnedOnCubesCount(instructions) == 590784)
  instructions2 = ReadRebootSequence('example2.txt')
  assert(RestartReactorAndGetTurnedOnCubesCountV2(instructions2) == 2758514936282235)


def SolvePartOne():
  turned_on_count = RestartReactorAndGetTurnedOnCubesCount(ReadRebootSequence('input.txt'))
  print(f'Part 1: Number of turned on cubes after restart = {turned_on_count}')
  assert(turned_on_count == 503864)


def SolvePartTwo():
  turned_on_count = RestartReactorAndGetTurnedOnCubesCountV2(ReadRebootSequence('input.txt'))
  print(f'Part 2: Number of turned on cubes after restart = {turned_on_count}')
  assert(turned_on_count == 1255547543528356)


def Main():
  print('Hello Day 22!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()