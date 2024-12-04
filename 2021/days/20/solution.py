#!/usr/bin/env python3 


def ReadInput(path):
  with open(path) as f:
    algorithm = f.readline().strip()
    empty_line = f.readline().strip()
    assert(empty_line == '')
    image = [line.strip() for line in f.readlines()]
    return algorithm, image


class Image(object):

  def __init__(self, algo, image, max_enhance_count=2):
    self.algo = algo
    original_width = len(image[0])
    padded_image = [''.join(['.'] * (original_width + max_enhance_count * 4)) for i in range(max_enhance_count * 2)]
    for line in image:
      padded_image.append(''.join(['.']) * max_enhance_count * 2 + line + (''.join(['.']) * max_enhance_count * 2))
    padded_image.extend([''.join(['.'] * (original_width + max_enhance_count * 4)) for i in range(max_enhance_count * 2)])
    self.padded_image = padded_image
    self.row_count = len(padded_image)
    self.col_count = len(padded_image[0])
    self.extended_value = '.'
    self.enhance_count = 0
    self.max_enhance_count = max_enhance_count

  def __str__(self):
    return '\n'.join(self.padded_image) + '\n'

  def _GetValue(self, row_idx, col_idx):
    if row_idx < 0 or row_idx >= self.row_count or col_idx < 0 or col_idx >= self.col_count:
      return self.extended_value
    else:
      return self.padded_image[row_idx][col_idx]

  def _GetThreeByThreeValue(self, row_idx, col_idx):
    value = 0
    for i in range(row_idx - 1, row_idx + 2):
      for j in range(col_idx - 1, col_idx + 2):
        value *= 2
        if self._GetValue(i, j) == '#':
          value += 1
    return value

  def Enhance(self):
    if self.enhance_count > self.max_enhance_count:
      raise Exception('Anyhow, you exceeded maximum enhancement count.')
    self.enhance_count += 1
    new_padded_image = []
    for i in range(self.row_count):
      new_row = []
      for j in range(self.col_count):
        value = self._GetThreeByThreeValue(i, j)
        new_row.append(self.algo[value])
      new_padded_image.append(''.join(new_row))
    self.padded_image = new_padded_image
    if self.extended_value == '.':
      self.extended_value = self.algo[0]
    else:
      self.extended_value = self.algo[2**9 - 1]
    return self

  def GetLitPixelCount(self):
    return sum([sum([1 if char == '#' else 0 for char in row]) for row in self.padded_image])


def Test():
  algo, image = ReadInput('example.txt')
  i = Image(algo, image).Enhance().Enhance()
  assert(i.GetLitPixelCount() == 35)
  algo, image = ReadInput('example.txt')
  i = Image(algo, image, max_enhance_count=50)
  for _ in range(50):
    i.Enhance()
  assert(i.GetLitPixelCount() == 3351)


def SolvePartOne():
  algo, image = ReadInput('input.txt')
  i = Image(algo, image).Enhance().Enhance()
  lit_pixels_count = i.GetLitPixelCount()
  print(f'Part 1: Lit pixels count after 2 rounds of enhancement = {lit_pixels_count}')
  assert(lit_pixels_count == 4964)


def SolvePartTwo():
  algo, image = ReadInput('input.txt')
  i = Image(algo, image, max_enhance_count=50)
  for _ in range(50):
    i.Enhance()
  lit_pixels_count = i.GetLitPixelCount()
  print(f'Part 2: Lit pixels count after 50 rounds of enhancement = {lit_pixels_count}')
  assert(lit_pixels_count == 13202)


def Main():
  print('Hello Day 20!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()