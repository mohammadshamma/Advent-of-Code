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


def CalculateProductOfTopThreeBasinsSizes(path):
  a = ReadHeightMap(path)
  visited = np.zeros(a.shape, dtype=bool)
  row_count, column_count = a.shape
  basin_sizes = []
  for i in range(row_count):
    for j in range(column_count):
      if IsLowPoint(a, i, j):
        # BFS the basin
        basin_size = 0
        to_visit = [(i, j)]
        while to_visit:
          current_i, current_j = to_visit.pop(0)
          if visited[current_i, current_j]:
            continue
          basin_size += 1
          visited[current_i, current_j] = True
          if current_i > 0 and a[current_i - 1, current_j] != 9 and not visited[current_i - 1, current_j]:
            to_visit.append((current_i - 1, current_j))
          if current_i < row_count - 1 and a[current_i + 1, current_j] != 9 and not visited[current_i + 1, current_j]:
            to_visit.append((current_i + 1, current_j))
          if current_j > 0 and a[current_i, current_j - 1] != 9 and not visited[current_i, current_j - 1]:
            to_visit.append((current_i, current_j - 1))
          if current_j < column_count - 1 and a[current_i, current_j + 1] != 9 and not visited[current_i, current_j + 1]:
            to_visit.append((current_i, current_j + 1))
        basin_sizes.append(basin_size)
  return np.prod(sorted(basin_sizes, reverse=True)[:3])


def Test():
  sum_of_risk_levels = CalculateLowPointsRiskLevels('test.txt')
  assert(sum_of_risk_levels == 15)
  product_of_top_three_basins_size = CalculateProductOfTopThreeBasinsSizes('test.txt')
  assert(product_of_top_three_basins_size == 1134)


def SolvePartOne():
  sum_of_risk_levels = CalculateLowPointsRiskLevels('height_map.txt')
  print(f'Sum of risk levels = {sum_of_risk_levels}')


def SolvePartTwo():
  p = CalculateProductOfTopThreeBasinsSizes('height_map.txt')
  print(f'Product of size of top three basins: {p}')


def Main():
  print('Hello Day 9!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()