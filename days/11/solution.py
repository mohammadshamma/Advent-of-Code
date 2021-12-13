#!/usr/bin/env python3 

import numpy as np


def ReadEnergyMap(path):
  return np.genfromtxt(path, dtype=int, delimiter=1)


def RunStep(energy_map):
  '''Run one step of time and return number of flashes and new energy map'''
  new_energy_map = energy_map + 1
  flashed = np.full(energy_map.shape, False)
  while True:
    flashed_updated = False
    large_indices = np.transpose(np.where(new_energy_map > 9))
    for x, y in large_indices:
      # print(f'x = {x}, y= {y}')
      if not flashed[x, y]:
        # print('Mark as flashed')
        flashed[x, y] = True
        for i in range(max(x - 1, 0), min(x + 2, new_energy_map.shape[0])):
          for j in range(max(y - 1, 0), min(y + 2, new_energy_map.shape[1])):
            # print(f'Incrementing i = {i}, j = {j}')
            new_energy_map[i][j] += 1
        flashed_updated = True
    if not flashed_updated:
      break
  new_energy_map[new_energy_map > 9] = 0
  return new_energy_map, (flashed == True).sum()


def GetTotalFlashesAfterNSteps(path, step_count):
  energy_map = ReadEnergyMap(path)
  total_flash_count = 0
  for i in range(100):
    energy_map, flash_count = RunStep(energy_map)
    total_flash_count += flash_count
  return total_flash_count


def GetFirstStepWhenAllOctopiFlash(path):
  energy_map = ReadEnergyMap(path)
  step = 0
  while True:
    energy_map, _ = RunStep(energy_map)
    step += 1
    if np.all(energy_map == 0):
      break
  return step


def Test():
  total_flashes = GetTotalFlashesAfterNSteps('example.txt', 100)
  assert(total_flashes == 1656)
  first_all_flash_step = GetFirstStepWhenAllOctopiFlash('example.txt')
  assert(first_all_flash_step == 195)


def SolvePartOne():
  total_flashes = GetTotalFlashesAfterNSteps('input.txt', 100)
  print(f'Total flashes after 100 steps = {total_flashes}')
  assert(total_flashes == 1697)


def SolvePartTwo():
  first_all_flash_step = GetFirstStepWhenAllOctopiFlash('input.txt')
  print(f'First all flash step = {first_all_flash_step}')
  assert(first_all_flash_step == 344)


def Main():
  print('Hello Day 11!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()