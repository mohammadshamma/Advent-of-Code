#!/usr/bin/env python3 

from copy import deepcopy
import math


def ReadSnailFishNumberStrings(path):
  with open(path) as f:
    return [line.strip() for line in f.readlines()]


def ParseSnailFishNumber(numbr_str):
  return [int(c) if c in '0123456789' else c for c in numbr_str]


def GetFirstTupleDeeperThanFourTuple(numbr_list):
  depth = 0
  for index in range(len(numbr_list)):
    if numbr_list[index] == '[':
      depth += 1
    elif numbr_list[index] == ']':
      depth -= 1
    if depth == 5:
      return index
  return None


def ExplodeTuple(numbr_list, index):
  numbr_list.pop(index)  # Left bracket
  left_number = numbr_list.pop(index)
  numbr_list.pop(index)  # comma
  right_number = numbr_list.pop(index)
  numbr_list.pop(index)  # Right bracket
  numbr_list.insert(index, 0)
  i = index - 1
  while i >= 0 and type(numbr_list[i]) is not int:
    i -= 1
  if i >= 0:
    numbr_list[i] += left_number
  i = index + 1
  while i < len(numbr_list) and type(numbr_list[i]) is not int:
    i += 1
  if i < len(numbr_list):
    numbr_list[i] += right_number
  return numbr_list


def GetFirstNumberGreaterThanNine(numbr_list):
  for i in range(len(numbr_list)):
    if type(numbr_list[i]) is int and numbr_list[i] > 9:
      return i
  return None


def SplitTuple(result, index):
  value = result.pop(index)  # Remove number
  left_value = math.floor(value / 2)
  right_value = math.ceil(value / 2)
  result.insert(index, ']')
  result.insert(index, right_value)
  result.insert(index, ',')
  result.insert(index, left_value)
  result.insert(index, '[')
  return result


def AddSnailFishNumbers(parsed_numbr_left, parsed_numbr_right):
  result = ['['] + parsed_numbr_left + [','] + parsed_numbr_right + [']']
  while True:
    index = GetFirstTupleDeeperThanFourTuple(result)
    if index != None:
      result = ExplodeTuple(result, index)
      continue
    index = GetFirstNumberGreaterThanNine(result)
    if index != None:
      result = SplitTuple(result, index)
      continue
    break
  return result


def AddManySnailFishNumbers(list_of_numbr_strs):
  parsed_numbers = [ParseSnailFishNumber(numbr_str) for numbr_str in list_of_numbr_strs]
  sum = parsed_numbers[0]
  for i in range(1, len(list_of_numbr_strs)):
    sum = AddSnailFishNumbers(sum, parsed_numbers[i])
  return UnparseSnailFishNumber(sum)


def ConvertNumberStringToPythonLists(numbr_str):
  if numbr_str[0] in '0123456789':
    assert(len(numbr_str) == 1)
    return int(numbr_str)
  
  depth = 0
  comma_position = None
  for i in range(len(numbr_str)):
    if numbr_str[i] == '[':
      depth += 1
    elif numbr_str[i] == ']':
      depth -= 1
    elif numbr_str[i] == ',' and depth == 1:
      comma_position = i
      break
  return [ConvertNumberStringToPythonLists(numbr_str[1:comma_position]), ConvertNumberStringToPythonLists(numbr_str[comma_position+1:-1])]


def CalculateMagnitude(numbr_in_lists):
  if type(numbr_in_lists) is int:
    return numbr_in_lists
  assert(len(numbr_in_lists) == 2)
  return 3 * CalculateMagnitude(numbr_in_lists[0]) + 2 * CalculateMagnitude(numbr_in_lists[1])


def CalculateMagnitudeForStr(numbr_str):
  number_in_lists = ConvertNumberStringToPythonLists(numbr_str)
  return CalculateMagnitude(number_in_lists)


def UnparseSnailFishNumber(numbr_list):
  return ''.join([str(element) if type(element) is not str else element for element in numbr_list])


def Test():
  assert(CalculateMagnitudeForStr(AddManySnailFishNumbers(ReadSnailFishNumberStrings('slightly_larger_example.txt'))) == 4140)


def SolvePartOne():
  sum_magnitude = CalculateMagnitudeForStr(AddManySnailFishNumbers(ReadSnailFishNumberStrings('input.txt')))
  print(f'Part 1: Sum magnitude = {sum_magnitude}')


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 18!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()