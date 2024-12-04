#!/usr/bin/env python3 

import math


def ProcessPartOneCommand(command, value, position, depth):
  if command == 'forward':
    return (position + value, depth)
  elif command == 'down':
    return (position, depth + value)
  elif command == 'up':
    return (position, max(depth - value, 0))
  else:
    raise Exception(f'Unrecognized command "{command}"')


def PartOneSolution():
  position = 0  # Horizontal position.
  depth = 0
  with open('input.txt') as f:
    for line in f.readlines():
      tokens = line.split(' ')
      assert(len(tokens) == 2)
      command = tokens[0]
      value = int(tokens[1])
      position, depth = ProcessPartOneCommand(command, value, position, depth)
  print(f'horizontal position = {position}, depth = {depth} (multiplication of both = {position * depth})')


def ProcessPartTwoCommand(command, value, position, depth, aim):
  if command == 'forward':
    return (position + value, max(depth + aim * value, 0), aim)
  elif command == 'down':
    return (position, depth, aim + value)
  elif command == 'up':
    return (position, depth, aim - value)
  else:
    raise Exception(f'Unrecognized command "{command}"')


def PartTwoSolution():
  position = 0  # Horizontal position.
  depth = 0
  aim = 0
  with open('input.txt') as f:
    for line in f.readlines():
      tokens = line.split(' ')
      assert(len(tokens) == 2)
      command = tokens[0]
      value = int(tokens[1])
      position, depth, aim = ProcessPartTwoCommand(command, value, position, depth, aim)
  print(f'horizontal position = {position}, depth = {depth}, aim = {aim} '
      f'(multiplication of position and depth = {position * depth})')


def Main():
  print('Hello Day1!')
  PartOneSolution()
  PartTwoSolution()


if __name__ == '__main__':
  Main()