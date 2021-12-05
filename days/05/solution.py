#!/usr/bin/env python3 

from collections import defaultdict


class Point(object):
  
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return hash(self.x + self.y * 1000)


class Line(object):

  def __init__(self, point_one, point_two):
    self.point_one = point_one
    self.point_two = point_two

  def IsVertical(self):
    return self.point_one.x == self.point_two.x

  def IsHorizontal(self):
    return self.point_one.y == self.point_two.y

  def GetPoints(self):
    if self.IsHorizontal():
      min_x = min(self.point_one.x, self.point_two.x)
      max_x = max(self.point_one.x, self.point_two.x)
      for x in range(min_x, max_x + 1):
        yield Point(x, self.point_one.y)
    elif self.IsVertical():
      min_y = min(self.point_one.y, self.point_two.y)
      max_y = max(self.point_one.y, self.point_two.y)
      for y in range(min_y, max_y + 1):
        yield Point(self.point_one.x, y)
    else:
      # Must be diagonal otherwise according to the requirements.
      x_step = 1 if self.point_one.x < self.point_two.x else -1
      y_step = 1 if self.point_one.y < self.point_two.y else -1
      x = self.point_one.x
      y = self.point_one.y
      while True:
        yield Point(x, y)
        if x == self.point_two.x:
          break
        x += x_step
        y += y_step


def ParsePointStr(point_str):
  coordinates = point_str.strip().split(',')
  assert(len(coordinates) == 2)
  return Point(int(coordinates[0]), int(coordinates[1]))


def ParseLineStr(line_str):
  points_str = line_str.split('->')
  assert(len(points_str) == 2)
  return Line(ParsePointStr(points_str[0]), ParsePointStr(points_str[1]))


def ParseLines():
  with open('input.txt') as f:
    return [ParseLineStr(line) for line in f.readlines()]


def SolvePartOne():
  lines = ParseLines()
  points_covered_counter = defaultdict(lambda: 0)
  for line in lines:
    if not line.IsHorizontal() and not line.IsVertical():
      continue
    for point in line.GetPoints():
      points_covered_counter[point] += 1
  dangerous_points_count = sum([1 if value >= 2 else 0 for value in points_covered_counter.values()])
  print(f'Part 1: dangerous points count (overlap of two or more) = {dangerous_points_count}')


def SolvePartTwo():
  lines = ParseLines()
  points_covered_counter = defaultdict(lambda: 0)
  for line in lines:
    for point in line.GetPoints():
      points_covered_counter[point] += 1
  dangerous_points_count = sum([1 if value >= 2 else 0 for value in points_covered_counter.values()])
  print(f'Part 2: dangerous points count (overlap of two or more) = {dangerous_points_count}')


def Main():
  print('Hello Day 5!')
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()