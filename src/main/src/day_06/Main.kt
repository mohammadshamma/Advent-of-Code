package day_06

import common.readInput
import java.util.LinkedList
import java.util.Queue

fun findStartMarker(input: String, distinctCharCount: Int): Int {
  val queue:Queue<Char> = LinkedList<Char>()
  var count = 0
  for (char in input) {
    count++
    queue.add(char)
    if (queue.size > distinctCharCount) {
      queue.remove()
    }
    if (queue.size == distinctCharCount) {
      // check if all characters are different
      val set = queue.toSet()
      if (set.size == distinctCharCount) {
        return count
      }
    }
  }
  assert(false)
  return -1
}

fun part1() {
  println("Part 1: ")
  val line = readInput("day_06/input_1.txt")
  val result = findStartMarker(line, 4)
  assert(result == 1134)
  println("Found 4 different characters at position $result")
}

fun part2() {
  println("Part 2: ")
  val line = readInput("day_06/input_1.txt")
  val result = findStartMarker(line, 14)
  assert(result == 2263)
  println("Found 14 different characters at position $result")
}

fun main() {
  println("Day 06")
  part1()
  part2()
}
