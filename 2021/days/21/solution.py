#!/usr/bin/env python3 


from collections import defaultdict

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


def CalculateWinningScenarios(players_pos, players_score, next_player, depth=0, cache={}):

  invocation_tuple = (players_pos[0], players_pos[1], players_score[0], players_score[1], next_player)
  if invocation_tuple in cache:
    return cache[invocation_tuple]

  scenario_counts = defaultdict(lambda: 0)
  for roll1 in range(1,4):
    for roll2 in range(1,4):
      for roll3 in range(1,4):
        scenario_counts[sum([roll1, roll2, roll3])] += 1
  
  player1_winning_outcomes = 0
  player2_winning_outcomes = 0
  for roll_sum, count in scenario_counts.items():
    # print(f'{"".join(["  "] * depth)}player {next_player} rolls {roll_sum} from {players_pos[next_player]}')
    new_pos = ((players_pos[next_player] + roll_sum  - 1) % 10) + 1
    new_score = players_score[next_player] + new_pos
    # print(f'{"".join(["  "] * depth)}player {next_player} new score {new_score} at {new_pos}')
    # print(f'{"".join(["  "] * depth)}players_score = {players_score}')
    if new_score >= 21:
      if next_player == 0:
        player1_winning_outcomes += count
      else:
        player2_winning_outcomes += count
    else:
      next_players_pos = players_pos.copy()
      next_players_score = players_score.copy()
      next_players_pos[next_player] = new_pos
      next_players_score[next_player] = new_score
      player1_wins, player2_wins = CalculateWinningScenarios(next_players_pos, next_players_score, (next_player + 1) % 2, depth=depth+1, cache=cache)
      player1_winning_outcomes += (player1_wins * count)
      player2_winning_outcomes += (player2_wins * count)

  cache[invocation_tuple] = (player1_winning_outcomes, player2_winning_outcomes)
  return player1_winning_outcomes, player2_winning_outcomes


def Test():
  g = Game(4, 8)
  g.Run()
  assert(g.GetLoserScoreAndRollCountProduct() == 739785)
  assert(CalculateWinningScenarios([4,8], [0,0], 0) == (444356092776315, 341960390180808))


def SolvePartOne():
  g = Game(2, 7)
  g.Run()
  print(f'Part 1: Loser\'s roll count and score product = {g.GetLoserScoreAndRollCountProduct()}')


def SolvePartTwo():
  scenario_counts = CalculateWinningScenarios([2,7], [0,0], 0)
  print(f'Part 2: Winners scenario count = {max(scenario_counts)}')
  assert(max(scenario_counts) == 133029050096658)

def Main():
  print('Hello Day 21!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()