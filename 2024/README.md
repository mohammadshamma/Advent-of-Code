# Advent of Code 2024!

This repository contains my solutions to the Advent of Code puzzles of 2024.

You can find the puzzles here: https://adventofcode.com/2024

This year, my theme will be using LLMs to write all the code. The goal here is I would not even tweak the code in any other way than changing my instructions to the LLM.

## Friends of mohammadshamma AoC 2024 repos

Please send a Pull Request and append yourself to the list below:

<!-- Please use the format [First and Last Names](http://gitgit/advent-of-code-repo.html) -->
* Append your repository here 

## Comparing LLM models' performance

I will be comparing the performance of different LLM models solving advent of code challenges.
I did not start using a consistent set of models until day 7, so I will only compare the models from day 7 onwards.
Each day, I will give the model the problem and ask it to generate a python program that would solve the problem.
I will then run the program and compare the results.
If the solution is not correct, I will review the generated code and try to understand why it is not correct.
I will then ask the model to generate a new program that would solve the problem.
I will repeat this process until the model generates a correct solution.
The number of conversation steps required to generate a correct solution will be recorded in the table below.

| Day | ChatGPT o1 conversation steps | Claude sonnet conversation steps | Gemini Advanced conversation steps |
| --- | ----------------------------- | -------------------------------- | ---------------------------------- |
| 7   | 1 + 1 = 2                     | 1 + 1 = 2                        | 1 + 1 = 2                          |
| 8   | 1 + 1 = 2                     | 3 + 2 = 5                        | 3 + 5 = 8                          |
| 9   | 5 + 1 = 6                     | 1 + 1 = 2                        | 5 + 16  = 21                       |
| 10  | 1 + 1 = 2                     | 1 + 1 = 2                        | 9 + 1 10                           |