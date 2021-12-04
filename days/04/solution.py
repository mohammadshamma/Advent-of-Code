#!/usr/bin/env python3 


class Board(object):
  def __init__(self, value_rows):
      self.value_rows = value_rows
      self.mark_rows = [[False for col in range(5)] for row in range(5)]
      self.solved = False

  def MarkAndCheck(self, value):
    for row in range(5):
      for col in range(5):
        if self.value_rows[row][col] == value:
          self.mark_rows[row][col] = True
          if all(self.mark_rows[row]) or all([self.mark_rows[i][col] for i in range(5)]):
            self.solved = True
            return value * sum([sum([self.value_rows[i][j] for j in range(5) if not self.mark_rows[i][j]]) for i in range(5)])

  def IsSolved(self):
    return self.solved


def ParseNumbers(file, sep=None):
  drawnNumbersText = file.readline()
  return [int(drawnNumber) for drawnNumber in drawnNumbersText.split(sep)]


def ParseBoard(file):
  rows = [ParseNumbers(file) for i in range(5)]
  return Board(rows)


def Main():
  print('Hello Day 4!')
  file = open('input.txt')
  drawn_numbers = ParseNumbers(file, ',')
  boards = []
  boards_solved = 0
  while file.readline():
    boards.append(ParseBoard(file))
  last_solved_board_score = None
  for drawn_number in drawn_numbers:
    for board in boards:
      if board.IsSolved():
        continue
      score = board.MarkAndCheck(drawn_number)
      if score: 
        boards_solved += 1
        if boards_solved == 1:
          print(f'Winning board score = {score}')
        last_solved_board_score = score
  if last_solved_board_score:
    print(f'Last solved board score = {last_solved_board_score}')


if __name__ == '__main__':
  Main()