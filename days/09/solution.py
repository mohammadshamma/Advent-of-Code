#!/usr/bin/env python3 

import numpy as np

def ReadHeightMap(path):
  return np.genfromtxt(path, dtype=int, delimiter=1)


def IsLowPoint(a, i, j):
  if i > 0 and a[i - 1, j] <= a[i, j]:
    return False
  if i < a.shape[0] - 1 and a[i + 1, j] <= a[i, j]:
    return False
  if j > 0 and a[i, j - 1] <= a[i, j]:
    return False
  if j < a.shape[1] - 1 and a[i, j + 1] <= a[i, j]:
    return False
  return True


def CalculateLowPointsRiskLevels(path):
  a = ReadHeightMap(path)
  row_count, column_count = a.shape
  sum_of_risk_levels = 0
  for i in range(row_count):
    for j in range(column_count):
      if IsLowPoint(a, i, j):
        sum_of_risk_levels += (a[i,j] + 1)
  return sum_of_risk_levels


def Test():
  sum_of_risk_levels = CalculateLowPointsRiskLevels('test.txt')
  assert(sum_of_risk_levels == 15)


def SolvePartOne():
  sum_of_risk_levels = CalculateLowPointsRiskLevels('height_map.txt')
  print(f'Sum of risk levels = {sum_of_risk_levels}')


def Main():
  print('Hello Day 9!')
  Test()
  SolvePartOne()
  # SolvePartTwo()


if __name__ == '__main__':
  Main()