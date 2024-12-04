package day_05

import common.readInput

class Stacks {

  private val stacks: Map<Int, MutableList<Char>>
  private val indices: List<Int>
  private val stackCount: Int

  // constructor that takes stack count and returns an array of empty mutable lists
  constructor(lines: List<String>) {
    // print indices line
    indices = lines[lines.size - 1].split(" ").filter { it.isNotEmpty() }.map { it.toInt() }
    stackCount = indices.size
    indices.map { Pair(it, mutableListOf<Char>()) }.toMap().let {
      stacks = it
    }
    lines.subList(0, lines.size - 1).reversed().forEach {
      indices.forEach { index ->
        val cargoValue = it[((index - 1) * 4) + 1]
        if (cargoValue != ' ') {
          stacks[index]!!.add(cargoValue)
        }
      }
    }

    fun toString(): String {
      val sb = StringBuilder()
      indices.forEach() {
        sb.append(it).append(": ")
        stacks[it]!!.forEach { sb.append(it).append(" ") }
        sb.append("/n")
      }
      sb.append("/n")
      return sb.toString()
    }
  }

  fun move(from: Int, to: Int) {
    stacks[to]!!.add(stacks[from]!!.removeAt(stacks[from]!!.size - 1))
  }
  private fun move(move: Move, preserveMovedItemOrders:Boolean = false) {
    if (preserveMovedItemOrders) {
      (move.count downTo 1).forEach() {
        stacks[move.to]!!.add(stacks[move.from]!![stacks[move.from]!!.size - it])
      }
      repeat(move.count) {
        stacks[move.from]!!.removeAt(stacks[move.from]!!.size - 1)
      }
    } else {
      for (i in 0 until move.count) {
        move(move.from, move.to)
      }
    }
  }

  fun move(moves: List<Move>, preserveMovedItemOrders:Boolean = false) {
    moves.forEach { move(it, preserveMovedItemOrders) }
  }

  fun printTopOfStacks() {
    indices.forEach {
      if (stacks[it]!!.size > 0) {
        print(stacks[it]!!.last())
      } else {
        print(" ")
      }
    }
    println()
  }
}

class Move(val count: Int, val from: Int, val to: Int) {
  companion object {
    fun parse(move: String): Move {
      val (count, from, to) = move.split(" ").filter { !(it == "move" || it == "from" || it == "to") }
      return Move(count.toInt(), from.toInt(), to.toInt())
    }
  }

  override fun toString(): String {
    return "Move $count from $from to $to"
  }
}

fun parseInput(lines: List<String>): Pair<Stacks, List<Move>> {
  val separatingLineIndex = lines.indexOf("")
  return Pair(Stacks(lines.subList(0, separatingLineIndex)), parseMoves(lines.subList(separatingLineIndex + 1, lines.size)))
}

fun parseMoves(lines: List<String>): List<Move> {
  return lines.map { Move.parse(it) }
}

fun part1() {
  println("Part 1: ")
  val(stacks, moves) = parseInput( readInput("day_05/input_1.txt").lines())
  stacks.move(moves)
  stacks.printTopOfStacks()
}

fun part2() {
  println("Part 2: ")
  val(stacks, moves) = parseInput( readInput("day_05/input_1.txt").lines())
  stacks.move(moves, preserveMovedItemOrders = true)
  stacks.printTopOfStacks()
}

fun main() {
  println("Hello Day 5!")
  part1()
  part2()
}
