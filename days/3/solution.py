#!/usr/bin/env python3 

READINGS_BIT_COUNT = 12

class PowerCalculator(object):
  
  def __init__(self):
    self.one_bit_counters = [0] * READINGS_BIT_COUNT
    self.values_count = 0

  def Add(self, value):
    for i in range(READINGS_BIT_COUNT):
      if (value & (1 << i)):
        self.one_bit_counters[i] += 1
    self.values_count += 1

  def CalculateResults(self):
    gamma_rate = 0
    for i in reversed(range(READINGS_BIT_COUNT)):
      gamma_rate = gamma_rate << 1
      if self.one_bit_counters[i] > (self.values_count / 2):
        gamma_rate |= 1
    epsilon_rate = gamma_rate ^ (2**READINGS_BIT_COUNT - 1)
    power = gamma_rate * epsilon_rate
    return (gamma_rate, epsilon_rate, power)


class LifeSupportRatingCalculator(object):

  O2_MODE = "o2_mode"
  CO2_MODE = "co2_mode"

  def __init__(self, values):
    self.values = values

  def _FilterList(self, mode, values, index):
    zero_values = []
    one_values = []
    for value in values:
      if value & (1 << index):
        one_values.append(value)
      else:
        zero_values.append(value)

    # Tie breaker
    if len(zero_values) == len(one_values):
      if mode == self.O2_MODE:
        return one_values
      else:
        return zero_values
    
    most_common_values = one_values if len(one_values) > len(zero_values) else zero_values
    least_common_values = one_values if len(one_values) < len(zero_values) else zero_values

    if mode == self.O2_MODE:
      return most_common_values
    elif mode == self.CO2_MODE:
      return least_common_values
    else:
      raise Exception('Any how: Unrecognized mode "{mode}"')

  def _CalculateRatingForMode(self, mode):
    local_values = self.values
    for i in reversed(range(READINGS_BIT_COUNT)):
      local_values = self._FilterList(mode, local_values, i)
      if len(local_values) == 1:
        return local_values[0]

  def CalculateResults(self):
    o2_generator_rating = self._CalculateRatingForMode(self.O2_MODE)
    co2_scrubber_rating = self._CalculateRatingForMode(self.CO2_MODE)
    life_support_rating = o2_generator_rating * co2_scrubber_rating
    return o2_generator_rating, co2_scrubber_rating, life_support_rating
  

def SolvePartOne():
  pc = PowerCalculator()
  with open('input.txt') as f:
    for line in f.readlines():
      value = int(line, 2)
      pc.Add(value)
  gamma_rate, epsilon_rate, power = pc.CalculateResults()
  print(f'Gamma rate = {gamma_rate}, Epsilon rate = {epsilon_rate}, Power = {power}')


def SolvePartTwo():
  values = []
  with open('input.txt') as f:
    for line in f.readlines():
      values.append(int(line, 2))
  lsrp = LifeSupportRatingCalculator(values)
  (o2_generator_rating, co2_scrubber_rating, life_support_rating) = lsrp.CalculateResults()
  print(f'O2 Generator Rating = {o2_generator_rating}, '
        f'CO2 Scrubber Rating = {co2_scrubber_rating}, '
        f'Life Support Rating = {life_support_rating}')


def Main():
  print('Hello Day 3!')
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()