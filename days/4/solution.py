#!/usr/bin/env python3 

class Board(object):
  def __init__(self, value_rows):
      self.value_rows = value_rows
      self.mark_rows = [[False for col in range(5)] for row in range(5)]


  def MarkAndCheck(self, value):
    for row in range(5):
      for col in range(5):
        if self.value_rows[row][col] == value:
          self.mark_rows[row][col] = True
          if all(self.mark_rows[row]) or all([self.mark_rows[i][col] for i in range(5)]):
            return value * sum([sum([self.value_rows[i][j] for j in range(5) if not self.mark_rows[i][j]]) for i in range(5)])


def ParseNumbers(file, sep=None):
  drawnNumbersText = file.readline()
  return [int(drawnNumber) for drawnNumber in drawnNumbersText.split(sep)]


def ParseBoard(file):
  rows = [ParseNumbers(file) for i in range(5)]
  return Board(rows)


def SolvePartOne():
  file = open('input.txt')
  drawn_numbers = ParseNumbers(file, ',')
  boards = []
  while file.readline():
    boards.append(ParseBoard(file))
  for drawn_number in drawn_numbers:
    for board in boards:
      score = board.MarkAndCheck(drawn_number)
      if score:
        print(f'winning board score = {score}')
        return


def Main():
  print('Hello Day 4!')
  SolvePartOne()


if __name__ == '__main__':
  Main()