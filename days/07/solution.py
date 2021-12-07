#!/usr/bin/env python3 


def GetCrabPositions(path):
  return [int(position) for position in open(path).readline().split(',')]


def CostFunctionV1(crab_position, to_position):
  return abs(crab_position - to_position)


# 1 -> 1 = n^2 - n(n-1)/2 = 1 - 0 = 1
# 2 -> 3 = 4 - 1 = 3
# 3 -> 6 = 9 - 3 = 6
def CostFunctionV2(crab_position, to_position):
  distance = abs(crab_position - to_position)
  return distance**2 - distance * (distance - 1) / 2


def CalculatePositionCost(crab_positions, position, cost_function):
  return sum([cost_function(crab_position, position) for crab_position in crab_positions])


def CalculateOptimalPosition(crab_positions, cost_function):
  minimum_position = min(crab_positions)
  maximum_position = max(crab_positions)
  optimal_cost = None
  optimal_position = None
  for position in range(minimum_position, maximum_position + 1):
    cost = CalculatePositionCost(crab_positions, position, cost_function)
    if not optimal_cost or cost < optimal_cost:
      optimal_cost = cost
      optimal_position = position
  return optimal_position, optimal_cost


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


def Main():
  print('Hello Day 7!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()