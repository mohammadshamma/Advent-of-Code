#!/usr/bin/env python3 

def ReadInput(path):
  hole_coordinates = []
  folds = []
  with open(path) as f:
    while True:
      l = f.readline().strip()
      if len(l) == 0:
        break
      parts = [int(part) for part in l.split(',')]
      assert(len(parts) == 2)
      hole_coordinates.append((parts[0], parts[1]))
  
    while True:
      l = f.readline().strip()
      if not l:
        break
      parts = l.split()
      assert(len(parts) == 3)
      assert(parts[0] == 'fold')
      assert(parts[1] == 'along')
      fold_parts = parts[2].split('=')
      assert(len(fold_parts) == 2)
      assert(fold_parts[0] in 'xy')
      folds.append((fold_parts[0], int(fold_parts[1])))
  return hole_coordinates, folds

def FoldHoles(hole_coordinates, fold_axis, fold_position):
  new_hole_coordinates = []
  for hole in hole_coordinates:
    if fold_axis == 'x':
      assert(fold_position != hole[0])
      new_hole_coordinates.append((hole[0] if fold_position > hole[0] else 2 * fold_position - hole[0], hole[1]))
    elif fold_axis == 'y':
      assert(fold_position != hole[1])
      new_hole_coordinates.append((hole[0], hole[1] if fold_position > hole[1] else 2 * fold_position - hole[1]))
    else:
      raise Exception(f'Anyhow, I was not expecting a fold axes value of "{fold_axis}"')
  return set(new_hole_coordinates)
      

def Test():
  hole_coordinates, folds = ReadInput('example.txt')
  for fold in folds:
    hole_coordinates = FoldHoles(hole_coordinates, fold[0], fold[1])


def SolvePartOne():
  hole_coordinates, folds = ReadInput('input.txt')
  hole_coordinates = FoldHoles(hole_coordinates, folds[0][0], folds[0][1])
  print(f'Points after one fold = {len(hole_coordinates)}')


def SolvePartTwo():
  hole_coordinates, folds = ReadInput('input.txt')
  for fold in folds:
    hole_coordinates = FoldHoles(hole_coordinates, fold[0], fold[1])
  max_x = max(hole[0] for hole in hole_coordinates)
  max_y = max(hole[1] for hole in hole_coordinates)
  folded_view = [['.' for x in range(max_x + 1)] for y in range(max_y + 1)]
  for hole in hole_coordinates:
    folded_view[hole[1]][hole[0]] = '#'
  for row in folded_view:
    print(''.join(row))
  

def Main():
  print('Hello Day 13!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()