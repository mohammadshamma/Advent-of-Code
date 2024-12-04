#!/usr/bin/env python3 


import math


def GetCrabPositions(path):
  return [int(position) for position in open(path).readline().split(',')]


def CostFunctionV1(crab_position, to_position):
  return abs(crab_position - to_position)


# 1 -> 1 = n^2 - n(n-1)/2 = 1 - 0 = 1
# 2 -> 3 = 4 - 1 = 3
# 3 -> 6 = 9 - 3 = 6
def CostFunctionV2(crab_position, to_position):
  distance = abs(crab_position - to_position)
  return int(distance**2 - distance * (distance - 1) / 2)


def CalculatePositionCost(crab_positions, position, cost_function):
  return sum([cost_function(crab_position, position) for crab_position in crab_positions])


def CalculateOptimalPosition(crab_positions, cost_function):
  minimum_position = min(crab_positions)
  maximum_position = max(crab_positions)
  minimum_position_cost = CalculatePositionCost(crab_positions, minimum_position, cost_function)
  maximum_position_cost = CalculatePositionCost(crab_positions, maximum_position, cost_function)
  while minimum_position < maximum_position - 1:
    middle_position_1 = math.floor((maximum_position + minimum_position)/2)
    middle_position_2 = middle_position_1 + 1
    middle_position_1_cost = CalculatePositionCost(crab_positions, middle_position_1, cost_function)
    middle_position_2_cost = CalculatePositionCost(crab_positions, middle_position_2, cost_function)
    if middle_position_1_cost < middle_position_2_cost:
      maximum_position = middle_position_1
      maximum_position_cost = middle_position_1_cost
    else:
      minimum_position = middle_position_2
      minimum_position_cost = middle_position_2_cost

  if maximum_position_cost < minimum_position_cost:
    return maximum_position, maximum_position_cost
  else:
    return minimum_position, minimum_position_cost


def Test():
  crab_positions = [16,1,2,0,4,2,7,1,2,14]
  optimal_position, optimal_cost = CalculateOptimalPosition(crab_positions, CostFunctionV1)
  assert(optimal_position == 2)
  assert(optimal_cost == 37)
  optimal_position, optimal_cost = CalculateOptimalPosition(crab_positions, CostFunctionV2)
  assert(optimal_position == 5)
  assert(optimal_cost == 168)


def SolvePartOne():
  crab_positions = GetCrabPositions('input.txt')
  optimal_position, optimal_cost = CalculateOptimalPosition(crab_positions, CostFunctionV1)
  print(f'Part I: Fuel cost = {optimal_cost}, position = {optimal_position}')
  assert(optimal_cost == 345035) 
  assert(optimal_position == 350)


def SolvePartTwo():
  crab_positions = GetCrabPositions('input.txt')
  optimal_position, optimal_cost = CalculateOptimalPosition(crab_positions, CostFunctionV2)
  print(f'Part II: Fuel cost = {optimal_cost}, position = {optimal_position}')
  assert(optimal_cost == 97038163) 
  assert(optimal_position == 478)


def BigBoy():
  crab_positions = GetCrabPositions('7-1000000-2.in')
  optimal_position, optimal_cost = CalculateOptimalPosition(crab_positions, CostFunctionV1)
  print(f'Big Boy Part I: Fuel cost = {optimal_cost}, position = {optimal_position}')
  assert(optimal_cost == 348121442862)
  optimal_position, optimal_cost = CalculateOptimalPosition(crab_positions, CostFunctionV2)
  print(f'Big Boy Part II: Fuel cost = {optimal_cost}, position = {optimal_position}')
  assert(optimal_cost == 97051441111920642)


def Main():
  print('Hello Day 7!')
  Test()
  SolvePartOne()
  SolvePartTwo()
  # To run the big boy dataset, download the input file from
  # https://the-tk.com/files/aoc2021-bigboys/7-1000000-2.in.xz
  # unzip it and uncomment the call below.
  # BigBoy()


if __name__ == '__main__':
  Main()