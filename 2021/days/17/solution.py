#!/usr/bin/env python3 

from dataclasses import dataclass
from typing import Tuple


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


def FindMinimumXVelocity(target: Target):
  velocity = 0
  while velocity < target.min_x:
    max_x_distance = velocity * (velocity + 1) / 2
    if max_x_distance >= target.min_x and max_x_distance <= target.max_x:
      return velocity
    velocity += 1
  return target.min_x


def VelocityHitsTarget(velocity_tuple: Tuple[int, int], target: Target):
  velocity_x = velocity_tuple[0]
  velocity_y = velocity_tuple[1]
  point_x = 0
  point_y = 0
  while point_x <= target.max_x and point_y >= target.min_y:
    if point_x >= target.min_x and point_y <= target.max_y:
      return True
    point_x += velocity_x
    if velocity_x > 0:
      velocity_x -= 1
    point_y += velocity_y
    velocity_y -= 1
  return False


def FindCountOfDistinctInitialVelocityShotsHittingTarget(target: Target):
  minimum_x_velocity = FindMinimumXVelocity(target)
  maximum_x_velocity = target.max_x
  minimum_y_velocity = target.min_y
  maximum_y_velocity = - target.min_y - 1
  
  potential_initial_velocity_tuples = []
  for x_velocity in range(minimum_x_velocity, maximum_x_velocity + 1):
    for y_velocty in range(minimum_y_velocity, maximum_y_velocity + 1): 
      potential_initial_velocity_tuples.append((x_velocity, y_velocty))
  possible_initial_velocity_tuples = [velocity_tuple for velocity_tuple in potential_initial_velocity_tuples if VelocityHitsTarget(velocity_tuple, target)]
  return len(possible_initial_velocity_tuples)


def Test():
  assert(FindMaxHeightOfShotsHittingTarget(EXAMPLE_TARGET) == 45)
  assert(FindCountOfDistinctInitialVelocityShotsHittingTarget(EXAMPLE_TARGET) == 112)


def SolvePartOne():
  max_height = FindMaxHeightOfShotsHittingTarget(INPUT_TARGET)
  print(f'Part 1: Maximum height of a shot hitting the target = {max_height}')
  assert(max_height == 8646)


def SolvePartTwo():
  possible_initial_velocities_count = FindCountOfDistinctInitialVelocityShotsHittingTarget(INPUT_TARGET)
  print(f'Part 2: Initial velocities count that hit the target = {possible_initial_velocities_count}')
  assert(possible_initial_velocities_count == 5945)
  

def Main():
  print('Hello Day 17!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()