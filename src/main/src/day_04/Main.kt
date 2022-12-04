package day_04

import common.readInput

class Range(private val start: Int, private val end: Int) {
  fun contains(value: Int): Boolean {
    return value in start..end
  }

  fun includesRange(range: Range): Boolean {
    return range.start >= start && range.end <= end
  }

  fun overlapsRange(range: Range): Boolean {
    return range.start <= end && range.end >= start
  }
}

fun parseRangePair(rangePair: String): Pair<Range, Range> {
  val (firstRange, secondRange) = rangePair.split(",")
  val (firstRangeStart, firstRangeEnd) = firstRange.split("-").map { it.toInt() }
  val (secondRangeStart, secondRangeEnd) = secondRange.split("-").map { it.toInt() }
  return Pair(Range(firstRangeStart, firstRangeEnd), Range(secondRangeStart, secondRangeEnd))
}

fun part1() {
  readInput("day_04/input_1.txt").lines().map { line ->
    val (firstRange, secondRange) = parseRangePair(line)
    firstRange.includesRange(secondRange)|| secondRange.includesRange(firstRange)
  }.count { it }.let {
    println("Part 1: The number of range pairs that include each other is $it")
    assert(it == 651)
  }
}

fun part2() {
  readInput("day_04/input_1.txt").lines().map { line ->
    val (firstRange, secondRange) = parseRangePair(line)
    firstRange.overlapsRange(secondRange)
  }.count { it }.let {
    println("Part 2: The number of range pairs that overlap each other is $it")
    assert(it == 956)
  }
}

fun main() {
  println("Hello Day 4!")
  part1()
  part2()
}
