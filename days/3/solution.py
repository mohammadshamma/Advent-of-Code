#!/usr/bin/env python3 

READINGS_BIT_COUNT = 12

class PowerCalculator(object):
  
  def __init__(self):
    self.one_bit_counters = [0] * READINGS_BIT_COUNT
    self.values_count = 0

  def add(self, value):
    for i in range(READINGS_BIT_COUNT):
      if (value & (1 << i)):
        self.one_bit_counters[i] += 1
    self.values_count += 1

  def calculateResults(self):
    gamma_rate = 0
    for i in reversed(range(READINGS_BIT_COUNT)):
      gamma_rate = gamma_rate << 1
      if self.one_bit_counters[i] > (self.values_count / 2):
        gamma_rate |= 1
    epsilon_rate = gamma_rate ^ (2**READINGS_BIT_COUNT - 1)
    power = gamma_rate * epsilon_rate
    return (gamma_rate, epsilon_rate, power)


def SolvePartOne():
  pc = PowerCalculator()
  with open('input.txt') as f:
    for line in f.readlines():
      value = int(line, 2)
      pc.add(value)
  gamma_rate, epsilon_rate, power = pc.calculateResults()
  print(f'Gamma rate = {gamma_rate}, Epsilon rate = {epsilon_rate}, Power = {power}')


def Main():
  print('Hello Day 3!')
  SolvePartOne()


if __name__ == '__main__':
  Main()