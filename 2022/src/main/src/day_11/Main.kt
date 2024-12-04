package day_11

import common.readInput
import java.math.BigInteger

class Monkey(
  private val number: Int,
  private val startingItems: List<BigInteger>,
  private val worryCalculator: (BigInteger) -> BigInteger,
  private val destinationCalculator: (BigInteger) -> Int,
  private val divisibleCheckNumber: Int,
  private val worryReduction: Boolean = true,
  private val modularWorryReduction: Boolean = false) {

  private var items = startingItems.toMutableList()
  private var inspectionCount = 0L
  private var modularStressReduction = -1

  fun runRound(): Map<Int, List<BigInteger>> {
    var results = HashMap<Int, List<BigInteger>>()
    while (items.size > 0) {
      val item = items.removeAt(0)
      val worry = when(worryReduction) {
        true -> worryCalculator(item) / 3.toBigInteger()
        false -> when(modularWorryReduction) {
          true -> worryCalculator(item) % modularStressReduction.toBigInteger()
          false -> worryCalculator(item)
        }
      }
      val destination = destinationCalculator(worry)
      results[destination] = results.getOrDefault(destination, listOf()).plus(worry)
      inspectionCount++
    }
    return results
  }

  fun appendItems(items: List<BigInteger>) {
    this.items.addAll(items)
  }

  fun getInspectionCount(): Long {
    return inspectionCount
  }

  fun getNumber(): Int {
    return number
  }

  fun getItems(): List<BigInteger> {
    return items
  }

  fun setModularStressReduction(modulo: Int) {
    modularStressReduction = modulo
  }

  fun getDivisibleCheckNumber(): Int {
    return divisibleCheckNumber
  }

  // factory method that parses the input
  companion object {
    fun parse(inputLines: List<String>, worryReduction: Boolean = true, modularWorryReduction: Boolean = false): Monkey {
      assert(inputLines.size == 6)
      val monkeyNumber: Int = inputLines[0].split(" ").let {
        assert(it.size == 2)
        assert(it[0] == "Monkey")
        it[1].endsWith(":")
        it[1].dropLast(1).toInt()
      }
      val startingItems = inputLines[1].let { line ->
        assert(line.startsWith("  Starting items: "))
        line.drop(18).split(", ").filter { it.isNotEmpty() }.map { it.trim().toBigInteger() }
      }
      val worryCalculator = inputLines[2].let { line ->
        assert(line.startsWith("  Operation: new = old "))
        val expression = line.drop(23)
        val tokens = expression.split(" ")
        assert(tokens.size == 2)
        val operator = tokens[0]
        when (tokens[1]) {
          "old" -> {
            when (operator) {
              "*" -> { old: BigInteger -> old * old }
              "+" -> { old: BigInteger -> old + old }
              else -> throw IllegalArgumentException("Unknown operator: $operator")
            }
          }
          else -> {
            val operand = tokens[1].toInt()
            when (operator) {
              "+" -> { old: BigInteger -> old + operand.toBigInteger() }
              "*" -> { old: BigInteger -> old * operand.toBigInteger() }
              else -> throw IllegalArgumentException("Unknown operator: $operator")
            }
          }
        }
      }
      val divisibleCheckNumber = inputLines[3].let { line ->
        assert(line.startsWith("  Test: divisible by "))
        line.drop(21).toInt()
      }
      val condition: (BigInteger) -> Boolean = inputLines[3].let { line ->
        {number:BigInteger -> number % divisibleCheckNumber.toBigInteger() == 0.toBigInteger()}
      }
      val positiveDestination = inputLines[4].let { line ->
        assert(line.startsWith("    If true: throw to monkey "))
        line.drop(29).toInt()
      }
      val negativeDestination = inputLines[5].let { line ->
        assert(line.startsWith("    If false: throw to monkey "))
        line.drop(30).toInt()
      }
      val destinationCalculator = { number: BigInteger -> if (condition(number)) positiveDestination else negativeDestination }
      return Monkey(monkeyNumber, startingItems, worryCalculator, destinationCalculator, divisibleCheckNumber, worryReduction=worryReduction, modularWorryReduction=modularWorryReduction)
    }
  }
}

class Monkeys(private val monkeys: Map<Int, Monkey>) {

  // static factory method that parses the input
  fun runRound(roundsCount: Int = 1) {
    for (round in 1..roundsCount) {
      for (monkey in monkeys.values) {
        val results = monkey.runRound()
        for ((destination, items) in results) {
          monkeys[destination]?.appendItems(items)
        }
      }
      // if round 1, 20 1000, 2000 ... etc, then print monkey inspection summary
      if (round == 1 || round == 20 || round %100 == 0 && round < 1000 || round % 1000 == 0) {
        println("== After round $round ==")
        for (monkey in monkeys.values) {
          println("Monkey ${monkey.getNumber()} inspected items ${monkey.getInspectionCount()} times")
        }
        println()
        for (monkey in monkeys.values) {
          println("Monkey ${monkey.getNumber()} has ${monkey.getItems().count()} count")
        }
        println()
      }
    }
  }

  fun getMonkeyBusinessLevel(): Long {
    // Get top 2 inspection counts and multiply them
    return monkeys.values.map { it.getInspectionCount() }.sortedDescending().take(2).reduce { acc, i -> acc * i }
  }

  companion object {
    fun parse(inputLines: List<String>, worryReduction: Boolean = true, modularWorryReduction: Boolean = false): Monkeys {
      val monkeys = HashMap<Int, Monkey>()
      inputLines.filter { it.isNotEmpty() }.chunked(6).forEach { chunk ->
        val monkey = Monkey.parse(chunk, worryReduction=worryReduction, modularWorryReduction=modularWorryReduction)
        assert(!monkeys.containsKey(monkey.getNumber()))
        monkeys[monkey.getNumber()] = monkey
      }
      // get product of getDivisibleCheckNumber of each monkey
      val modularStressReduction = monkeys.values.map { it.getDivisibleCheckNumber() }.reduce { acc, i -> acc * i }
      println("Modular stress reduction: $modularStressReduction")
      for (monkey in monkeys.values) {
        monkey.setModularStressReduction(modularStressReduction)
      }
      return Monkeys(monkeys)
    }
  }
}

fun solvePart1(path: String): Long {
  val inputLines = readInput(path).lines()
  val monkeys = Monkeys.parse(inputLines)
  monkeys.runRound(20)
  return monkeys.getMonkeyBusinessLevel()
}

fun part1() {
  println("Part 1:")
  solvePart1("day_11/sample.txt").let { println("Sample monkey business level: $it") }
  solvePart1("day_11/input.txt").let {
    println("Input monkey business level: $it")
    assert(it == 64032L)
  }
}

fun solvePart2(path: String): Long {
  val inputLines = readInput(path).lines()
  val monkeys = Monkeys.parse(inputLines, worryReduction=false, modularWorryReduction=true)
  monkeys.runRound(10000)
  return monkeys.getMonkeyBusinessLevel()
}

fun compareOptimizedVsNotOptimized(path: String) {
  val inputLines = readInput(path).lines()
  val monkeys1 = Monkeys.parse(inputLines, worryReduction = false)
  monkeys1.runRound(700)
  println("monkeys.getMonkeyBusinessLevel() = ${monkeys1.getMonkeyBusinessLevel()}")
  val monkeys2 = Monkeys.parse(inputLines, worryReduction=false, modularWorryReduction=true)
  monkeys2.runRound(700)
  println("monkeys.getMonkeyBusinessLevel() = ${monkeys2.getMonkeyBusinessLevel()}")
}

fun part2() {
  println("Part 2:")
//  compareOptimizedVsNotOptimized("day_11/sample.txt")
  solvePart2("day_11/sample.txt").let { println("Sample monkey business level: $it") }
  solvePart2("day_11/input.txt").let {
    println("Input monkey business level: $it")
    assert(it == 12729522272)
  }
}

fun main() {
  println("Day 11")
  part1()
  part2()
}
