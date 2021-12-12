#!/usr/bin/env python3 


from collections import defaultdict
from copy import copy


START = 'start'
END = 'end'

class AdjacencyListGraph(object):

  def __init__(self, connections):
    self._adjacency_lists = defaultdict(list)
    for connection in connections:
      self._adjacency_lists[connection[0]].append(connection[1])
      self._adjacency_lists[connection[1]].append(connection[0])

  def GetAllPossiblePaths(self, starting_vertex, final_vertex):
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
          possible_next_steps = [vertex for vertex in self._adjacency_lists[vertex_stack[-1]] if vertex.isupper() or vertex not in vertex_stack]
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
  possible_paths = g1.GetAllPossiblePaths(START, END)
  assert(len(possible_paths) == 10)
  g2 = AdjacencyListGraph(ReadConnectionList('example2.txt'))
  assert(len(g2.GetAllPossiblePaths(START, END)) == 19)
  g3 = AdjacencyListGraph(ReadConnectionList('example3.txt'))
  assert(len(g3.GetAllPossiblePaths(START, END)) == 226)


def SolvePartOne():
  g = AdjacencyListGraph(ReadConnectionList('input.txt'))
  all_paths = g.GetAllPossiblePaths(START, END)
  print(f'The count of all pahts is = {len(all_paths)}')
  assert(len(all_paths) == 3369)


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 10!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()