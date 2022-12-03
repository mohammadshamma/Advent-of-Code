package day_03

import common.readInput

fun getRuckSackTwoCompartments(rucksackContents: String): Pair<String, String> {
  assert(rucksackContents.length % 2 == 0)
  val firstCompartment = rucksackContents.substring(0, rucksackContents.length / 2)
  val secondCompartment = rucksackContents.substring(rucksackContents.length / 2)
  return Pair(firstCompartment, secondCompartment)
}

fun calculateCharacterPriority(item: Char): Int {
  return if (item.isLowerCase()) {
    // a = 1, b = 2, c = 3, etc.
    item.code - 96
  } else {
    // A = 27, B = 28, C = 29, etc.
    item.code - 64 + 26
  }
}

fun getOverlappingItem(firstCompartment: String, secondCompartment: String): Char? {
  val firstCompartmentItems = firstCompartment.toCharArray().toSet()
  val secondCompartmentItems = secondCompartment.toCharArray().toSet()
  val overlappingItems = firstCompartmentItems.intersect(secondCompartmentItems)
  return if (overlappingItems.isEmpty()) {
    null
  } else {
    overlappingItems.first()
  }
}

fun sumOverlappingItemsPriorities(lines: List<String>): Int {
  return lines.map { line ->
    val (firstCompartment, secondCompartment) = getRuckSackTwoCompartments(line)
    val overlappingItem = getOverlappingItem(firstCompartment, secondCompartment)
    if (overlappingItem != null) {
      calculateCharacterPriority(overlappingItem)
    } else {
      0
    }
  }.sum()
}

fun part1() {
  val sampleLines = listOf(
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
  )
  sumOverlappingItemsPriorities(sampleLines).let {
    println("Part 1: Sample lines sum: $it")
    assert(it == 157)
  }
  sumOverlappingItemsPriorities(readInput("day_03/input_1.txt").lines()).let {
    println("Part 1: The sum of overlapping items priorities is $it")
    assert(it == 7845)
  }
}

fun findCommonItemInRucksacks(vararg rucksacks: String): Char {
  val rucksacksItems = rucksacks.map { it.toCharArray().toSet() }
  val commonItems = rucksacksItems.reduce { acc, set -> acc.intersect(set) }
  assert(commonItems.size == 1)
  return commonItems.first()
}
fun sumGroupBadgesPriorities(lines: List<String>): Int {
  return lines.chunked(3).map {
    calculateCharacterPriority(findCommonItemInRucksacks(it[0], it[1], it[2]))
  }.sum()
}

fun part2() {
  sumGroupBadgesPriorities(readInput("day_03/input_1.txt").lines()).let {
    println("Part 2: The sum of group badges priorities is $it")
    assert(it == 2790)
  }
}

fun main() {
  println("Hello Day 3!")
  part1()
  part2()
}
