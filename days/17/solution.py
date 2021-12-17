#!/usr/bin/env python3 

from dataclasses import dataclass


@dataclass
class Target:
    """Class for keeping track of an item in inventory."""
    min_y: int
    max_y: int
    min_x: int
    max_x: int


EXAMPLE_TARGET = Target(min_y=-10, max_y=-5, min_x=20, max_x=30)

INPUT_TARGET = Target(min_y=-132, max_y=-72, min_x=155, max_x=215)

def FindMaxHeightOfShotsHittingTarget(target: Target):
  initial_y_velocity = - target.min_y - 1
  max_height = sum([v for v in range(initial_y_velocity + 1)])
  return max_height


def Test():
  assert(FindMaxHeightOfShotsHittingTarget(EXAMPLE_TARGET) == 45)


def SolvePartOne():
  max_height = FindMaxHeightOfShotsHittingTarget(INPUT_TARGET)
  print(f'Part 1: Maximum height of a shot hitting the target = {max_height}')
  assert(max_height == 8646)


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 17!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()