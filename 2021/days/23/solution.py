#!/usr/bin/env python3 

from collections import defaultdict
import heapq as heap


STACK_COLUMNS = (3, 5, 7, 9)
CORRIDOR_ROW = 1

AMPHIPOD_MULTIPLIER = {
  'A': 1,
  'B': 10,
  'C': 100,
  'D': 1000,
}

AMPHIPOD_TO_COL = {
  'A': 3,
  'B': 5,
  'C': 7,
  'D': 9,
}


def ReadMap(path):
  with open(path) as f:
    return [line for line in f.readlines()]


def PrintMap(map):
  [print(row, end='') for row in map]
  print('')


def GetHashableMap(map):
  return tuple(map)


def GetTopOfStacks(map):
  top_of_stack_starting_points = []
  row_count = len(map)
  for col in STACK_COLUMNS:
    for row in range(2, row_count - 1):
      if map[row][col] in AMPHIPOD_TO_COL.keys():
        top_of_stack_starting_points.append((row, col))
        break
  return top_of_stack_starting_points


def GetPossibleTopOfStackMoves(start_point, map):

  end_points = []
  # Check right slots.
  for i in range(start_point[1], len(map[1])):
    if i in STACK_COLUMNS:
      continue
    if map[CORRIDOR_ROW][i] != '.':
      break
    end_points.append((CORRIDOR_ROW, i))

  # Check left slots.
  for i in range(start_point[1], 0, -1):
    if i in STACK_COLUMNS:
      continue
    if map[CORRIDOR_ROW][i] != '.':
      break
    end_points.append((CORRIDOR_ROW, i))
  
  return [(start_point, end_point) for end_point in end_points]


def GetCorridorStartingPoints(map):
  start_points = []
  for col in range(len(map[CORRIDOR_ROW])):
    if map[CORRIDOR_ROW][col] in AMPHIPOD_TO_COL.keys():
      start_points.append((CORRIDOR_ROW, col))
  return start_points


def GetPossibleCorridorMove(start_point, map):
  amphipod = map[start_point[0]][start_point[1]]
  destination_col = AMPHIPOD_TO_COL[amphipod]
  if destination_col > start_point[1]:
    for col in range(start_point[1] + 1, destination_col):
      if map[start_point[0]][col] != '.':
        return None
  else:
    for col in range(destination_col, start_point[1]):
      if map[start_point[0]][col] != '.':
        return None

  row_count = len(map)
  for row in range(row_count - 2, 1, -1):
    if map[row][destination_col] == '.':
      return (start_point, (row, destination_col))
    if map[row][destination_col] != amphipod:
      break
  return None


def GetPossibleMoves(map):

  possible_moves = []

  # Check moves starting from a top of stack.
  top_of_stack_starting_points = GetTopOfStacks(map)
  for top_of_stack_starting_point in top_of_stack_starting_points:
    top_of_stack_possible_moves = GetPossibleTopOfStackMoves(top_of_stack_starting_point, map)
    possible_moves.extend(top_of_stack_possible_moves)

  # Check moves starting from a corridor spot.
  corridor_starting_points = GetCorridorStartingPoints(map)
  for corridor_starting_point in corridor_starting_points:
    possible_move = GetPossibleCorridorMove(corridor_starting_point, map)
    if possible_move:
      return [possible_move]

  return possible_moves


def GetMoveCost(move, map):
  start_point = move[0]
  end_point = move[1]
  amphipod = map[start_point[0]][start_point[1]]
  return (abs(start_point[0] - end_point[0]) + abs(start_point[1] - end_point[1])) * AMPHIPOD_MULTIPLIER[amphipod]


def GetMapAfterMove(move, map):
  start_point = move[0]
  end_point = move[1]
  amphipod = map[start_point[0]][start_point[1]]
  new_map = map.copy()
  start_row = new_map[start_point[0]]
  new_map[start_point[0]] = ''.join([start_row[:start_point[1]], '.', start_row[start_point[1] + 1:]])
  end_row = new_map[end_point[0]]
  new_map[end_point[0]] = ''.join([end_row[:end_point[1]], amphipod, end_row[end_point[1] + 1:]])
  return new_map


def MapIsSolved(map):
  for amphipod, col in AMPHIPOD_TO_COL.items():
    if map[2][col] != amphipod or map[3][col] != amphipod:
      return False
  return True


def GetMinimumCostToFixArrangement(initial_map):
  visited = set()
  pq = []
  parent_map = defaultdict(lambda: None)
  nodeCosts = defaultdict(lambda: float('inf'))
  nodeCosts[GetHashableMap(initial_map)] = 0
  heap.heappush(pq, (0, initial_map))
 
  while pq:
    # go greedily by always extending the shorter cost nodes first
    _, map = heap.heappop(pq)
    hashable_map = GetHashableMap(map)
    visited.add(hashable_map)

    if MapIsSolved(map):
      steps = []
      current_map = hashable_map
      while current_map is not None:
        steps.append(current_map)
        if current_map == parent_map[current_map]:
          assert(False)
        current_map = parent_map[current_map]
      return nodeCosts[hashable_map], reversed(steps)
 
    for move, cost in [(move, GetMoveCost(move, map)) for move in GetPossibleMoves(map)]:
      next_map = GetMapAfterMove(move, map)
      hashable_next_map = GetHashableMap(next_map)

      if hashable_next_map in visited:
        continue
        
      newCost = nodeCosts[hashable_map] + cost
      if nodeCosts[hashable_next_map] > newCost:
        parent_map[hashable_next_map] = hashable_map
        nodeCosts[hashable_next_map] = newCost
        heap.heappush(pq, (newCost, next_map))
        
  return None


def Test():
  map = ReadMap('example.txt')
  min_cost, steps = GetMinimumCostToFixArrangement(map)
  assert(min_cost == 12521)

  map = ReadMap('example2.txt')
  min_cost, steps = GetMinimumCostToFixArrangement(map)
  assert(min_cost == 44169)


def SolvePartOne():
  map = ReadMap('input.txt')
  min_cost, steps = GetMinimumCostToFixArrangement(map)
  print(f'Part 1: Minimum cost to move amphipods: {min_cost}')
  assert(min_cost == 15299)


def SolvePartTwo():
  map = ReadMap('input2.txt')
  min_cost, steps = GetMinimumCostToFixArrangement(map)
  print(f'Part 2: Minimum cost to move amphipods: {min_cost}')
  assert(min_cost == 47193)


def Main():
  print('Hello Day 23!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()