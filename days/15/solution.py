#!/usr/bin/env python3 


from collections import defaultdict
import heapq as heap
import numpy as np


def ReadRiskLevelMap(path):
  return np.genfromtxt(path, dtype=int, delimiter=1)


def GetPointNeighbours(point, shape):
  neighbours = []
  if point[0] > 0:
    neighbours.append((point[0] - 1, point[1]))
  if point[1] > 0:
    neighbours.append((point[0], point[1] - 1))
  if point[0] < shape[0] - 1:
    neighbours.append((point[0] + 1, point[1]))
  if point[1] < shape[1] - 1:
    neighbours.append((point[0], point[1] + 1))
  return neighbours


def GetShortestPathRiskLevel(array):
  visited = set()
  parentsMap = {}
  pq = []
  nodeCosts = defaultdict(lambda: float('inf'))
  nodeCosts[(0, 0)] = 0
  heap.heappush(pq, (0, (0, 0)))
 
  while pq:
    # go greedily by always extending the shorter cost nodes first
    _, node = heap.heappop(pq)
    visited.add(node)
 
    for adjNode, weight in [(adjacent_node, array[adjacent_node]) for adjacent_node in GetPointNeighbours(node, array.shape)]:
      if adjNode in visited:	continue
        
      newCost = nodeCosts[node] + weight
      if nodeCosts[adjNode] > newCost:
        parentsMap[adjNode] = node
        nodeCosts[adjNode] = newCost
        heap.heappush(pq, (newCost, adjNode))
        
  return nodeCosts[array.shape[0] - 1, array.shape[1] - 1]


def GetNextArray(array):
  return (array % 9) + 1

def ExpandArray(array):
  # Generate top 5 arrays and concatenate them.
  top_arrays_list = [array]
  top_arrays_list.append(GetNextArray(top_arrays_list[-1]))
  top_arrays_list.append(GetNextArray(top_arrays_list[-1]))
  top_arrays_list.append(GetNextArray(top_arrays_list[-1]))
  top_arrays_list.append(GetNextArray(top_arrays_list[-1]))
  top_array = np.concatenate(top_arrays_list, axis=1)

  # Generate lower arrays 4 times downwards and concatenate them.
  all_arrays_list = [top_array]
  all_arrays_list.append(GetNextArray(all_arrays_list[-1]))
  all_arrays_list.append(GetNextArray(all_arrays_list[-1]))
  all_arrays_list.append(GetNextArray(all_arrays_list[-1]))
  all_arrays_list.append(GetNextArray(all_arrays_list[-1]))
  return np.concatenate(all_arrays_list, axis=0)


def Test():
  # Part 1
  array = ReadRiskLevelMap('example.txt')
  risk_level = GetShortestPathRiskLevel(array)
  assert(risk_level == 40)
  # Part 2
  array = ReadRiskLevelMap('example.txt')
  big_array = ExpandArray(array)
  risk_level = GetShortestPathRiskLevel(big_array)
  assert(risk_level == 315)


def SolvePartOne():
  array = ReadRiskLevelMap('input.txt')
  minimum_risk_level = GetShortestPathRiskLevel(array)
  print(f'Part 1: Minimum risk level = {minimum_risk_level}')
  assert(minimum_risk_level == 739)


def SolvePartTwo():
  array = ReadRiskLevelMap('input.txt')
  big_array = ExpandArray(array)
  minimum_risk_level = GetShortestPathRiskLevel(big_array)
  print(f'Part 2: Minimum risk level in big array = {minimum_risk_level}')
  assert(minimum_risk_level == 3040)


def Main():
  print('Hello Day 15!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()