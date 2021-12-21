#!/usr/bin/env python3 

class PredictableDice(object):

  def __init__(self):
    self.next_roll = 1
    self.roll_count = 0

  def Roll(self):
    value = self.next_roll
    self.next_roll = (self.next_roll % 100) + 1
    self.roll_count += 1
    return value

  def GetRollCount(self):
    return self.roll_count


class Player(object):

  def __init__(self, position):
    self.position = position
    self.score = 0

  def GetScore(self):
    return self.score

  def PlayRound(self, rolls):
    roll_sum = sum(rolls)
    self.position = ((self.position + roll_sum  - 1) % 10) + 1
    self.score += self.position
    game_ended = False
    if self.score >= 1000:
      game_ended = True
    return game_ended, self.position, self.score


class Game(object):

  def __init__(self, player_one_starting_position, player_two_starting_position):
    self.next_player = 0
    self.dice = PredictableDice()
    self.players = [Player(player_one_starting_position), Player(player_two_starting_position)]

  def Run(self):
    while True:
      rolls = [self.dice.Roll() for _ in range(3)]
      game_ended, position, score = self.players[self.next_player].PlayRound(rolls)
      # print(f'Player {self.next_player} rolled {rolls} and moved to space {position} for a total score of {score}')
      if game_ended:
        break
      self.next_player += 1
      self.next_player %= len(self.players)

  def GetLoserScoreAndRollCountProduct(self):
    assert(len(self.players) == 2)
    loser_index = 1
    if self.players[0].GetScore() < 1000:
      loser_index = 0 
    return self.players[loser_index].GetScore() * self.dice.GetRollCount()


def Test():
  g = Game(4, 8)
  g.Run()
  assert(g.GetLoserScoreAndRollCountProduct() == 739785)


def SolvePartOne():
  g = Game(2, 7)
  g.Run()
  print(f'Part 1: Loser\'s roll count and score product = {g.GetLoserScoreAndRollCountProduct()}')


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 21!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()