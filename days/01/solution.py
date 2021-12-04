#!/usr/bin/env python3 

def PartOneSolution():
  increase_count = 0
  with open('input.txt') as f:
    last_value = None
    for line in f.readlines():
      current_value = int(line)
      if last_value:
        if current_value > last_value:
          increase_count += 1
      last_value = current_value
  print(f'One measure increase count = {increase_count}')  

def PartTwoSolution():
  increase_count = 0
  with open('input.txt') as f:
    buffer = []
    for line in f.readlines():
      current_value = int(line)

      if len(buffer) != 3:
        buffer.append(current_value)
        continue

      if buffer[0] < current_value:
        increase_count += 1
      
      buffer.pop(0)
      buffer.append(current_value)
    
  print(f'Window of three measure increase count = {increase_count}')  

def Main():
  print('Hello Day1!')
  PartOneSolution()
  PartTwoSolution()


if __name__ == '__main__':
  Main()