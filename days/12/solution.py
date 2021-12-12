#!/usr/bin/env python3 


from collections import defaultdict
from copy import copy


START = 'start'
END = 'end'

class AdjacencyListGraph(object):

  POLICY_SMALL_CAVES_ONCE = 'small_caves_once'
  POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE = 'one_small_cave_twice_rest_once'
  ALL_POLICIES = [POLICY_SMALL_CAVES_ONCE, POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE]

  def __init__(self, connections):
    self._adjacency_lists = defaultdict(list)
    for connection in connections:
      self._adjacency_lists[connection[0]].append(connection[1])
      self._adjacency_lists[connection[1]].append(connection[0])

  def _IsValidNextStep(vertex_stack, new_vertex, policy):
    if policy == AdjacencyListGraph.POLICY_SMALL_CAVES_ONCE:
      return new_vertex.isupper() or new_vertex not in vertex_stack
    elif policy == AdjacencyListGraph.POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE:
      small_vertex_counter = defaultdict(lambda: 0)
      if not new_vertex.isupper():
        small_vertex_counter[new_vertex] += 1
      for vertex in vertex_stack:
        if not vertex.isupper():
          small_vertex_counter[vertex] += 1
      if small_vertex_counter[START] > 1 or small_vertex_counter[END] > 1:
        return False
      if len([count for count in small_vertex_counter.values() if count > 1]) > 1:
        return False
      if len([count for count in small_vertex_counter.values() if count > 2]) > 0:
        return False
      return True
    else:
      raise Exception(f'Anyhow, you might have forgotten to implement for the potentially new policy {policy}')

  def GetAllPossiblePaths(self, starting_vertex, final_vertex, policy=POLICY_SMALL_CAVES_ONCE):
    possible_paths = []
    vertex_stack = [starting_vertex]
    possible_next_steps_stack = []
    possible_next_steps_index_stack = []
    possible_next_steps = None
    possible_next_steps_index = None
    while True:
      if vertex_stack[-1] == final_vertex:
        possible_paths.append(copy(vertex_stack))
        vertex_stack.pop()
        possible_next_steps = possible_next_steps_stack.pop()
        possible_next_steps_index = possible_next_steps_index_stack.pop()
      else:
        if not possible_next_steps:
          possible_next_steps = [vertex for vertex in self._adjacency_lists[vertex_stack[-1]] if AdjacencyListGraph._IsValidNextStep(vertex_stack, vertex, policy)]
          possible_next_steps_index = -1
        possible_next_steps_index += 1
        if possible_next_steps_index == len(possible_next_steps):
          if not possible_next_steps_stack:
            break
          possible_next_steps = possible_next_steps_stack.pop()
          possible_next_steps_index = possible_next_steps_index_stack.pop()
          vertex_stack.pop()
        else:        
          vertex_stack.append(possible_next_steps[possible_next_steps_index])
          possible_next_steps_stack.append(possible_next_steps)
          possible_next_steps_index_stack.append(possible_next_steps_index)
          possible_next_steps = None
          possible_next_steps_index = None
    return possible_paths


def ReadConnectionList(path):
  with open(path) as f:
    lines = f.readlines()
    adjacency_list = []
    for line in lines:
      parts = line.strip().split("-")
      assert(len(parts) == 2)
      adjacency_list.append((parts[0], parts[1]))
    return adjacency_list


def Test():
  adjacency_list = ReadConnectionList('example1.txt')
  g1 = AdjacencyListGraph(adjacency_list)
  assert(len(g1.GetAllPossiblePaths(START, END)) == 10)
  assert(len(g1.GetAllPossiblePaths(START, END, AdjacencyListGraph.POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE)) == 36)
  g2 = AdjacencyListGraph(ReadConnectionList('example2.txt'))
  assert(len(g2.GetAllPossiblePaths(START, END)) == 19)
  assert(len(g2.GetAllPossiblePaths(START, END, AdjacencyListGraph.POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE)) == 103)
  g3 = AdjacencyListGraph(ReadConnectionList('example3.txt'))
  assert(len(g3.GetAllPossiblePaths(START, END)) == 226)
  assert(len(g3.GetAllPossiblePaths(START, END, AdjacencyListGraph.POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE)) == 3509)


def SolvePartOne():
  g = AdjacencyListGraph(ReadConnectionList('input.txt'))
  all_paths = g.GetAllPossiblePaths(START, END)
  print(f'The count of all pahts is = {len(all_paths)}')
  assert(len(all_paths) == 3369)


def SolvePartTwo():
  g = AdjacencyListGraph(ReadConnectionList('input.txt'))
  all_paths = g.GetAllPossiblePaths(START, END, AdjacencyListGraph.POLICY_ONE_SMALL_CAVE_TWICE_REST_ONCE)
  print(f'The count of all pahts is = {len(all_paths)}')
  assert(len(all_paths) == 85883)


def Main():
  print('Hello Day 10!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()