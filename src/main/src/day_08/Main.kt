package day_08

import common.readInput

class Forrest(private val rows: List<String>) {

  private val grid = rows.map { it.toCharArray().map { it.toString().toInt() } }

  fun get(x: Int, y: Int): Int {
    return grid[y][x]
  }

  fun width(): Int {
    return grid[0].size
  }

  fun height(): Int {
    return grid.size
  }

  private fun treeIsVisible(x: Int, y: Int): Boolean {
    // if position is on the edge of the grid, it is visible
    if (x == 0 || x == width() - 1 || y == 0 || y == height() - 1) {
      return true
    }
    // else if tree is taller than every tree on the line between it and any edge, it is visible
    val treeHeight = grid[y][x]
    (0 until x)
      .map { grid[y][it] }.all { treeHeight > it }.let { if (it) return true }
    (x + 1 until width())
      .map { grid[y][it] }.all { treeHeight > it }.let { if (it) return true }
    (0 until y)
      .map { grid[it][x] }.all { treeHeight > it }.let { if (it) return true }
    (y + 1 until height())
      .map { grid[it][x] }.all { treeHeight > it }.let { if (it) return true }
    return false
  }

  fun visibleTrees(): Int {
    var count = 0
    for (y in 0 until height()) {
      for (x in 0 until width()) {
        if (treeIsVisible(x, y)) {
          count++
        }
      }
    }
    return count
  }

  fun treeScenicScore(x: Int, y: Int): Int {
    // If tree is on edge of grid, score is 0
    if (x == 0 || x == width() - 1 || y == 0 || y == height() - 1) {
      return 0
    }
    // Calculate the number of trees visible in each direction.
    val treeHeight = grid[y][x]
    val topVisibleTrees = (y - 1 downTo 0).indexOfFirst { grid[it][x] >= treeHeight }.let { if (it == -1) y else it + 1 }
    val bottomVisibleTrees = (y + 1 until height()).indexOfFirst { grid[it][x] >= treeHeight }.let { if (it == -1) height() - 1 - y else it + 1 }
    val leftVisibleTrees = (x - 1 downTo 0).indexOfFirst { grid[y][it] >= treeHeight }.let { if (it == -1) x else it + 1 }
    val rightVisibleTrees = (x + 1 until width()).indexOfFirst { grid[y][it] >= treeHeight }.let { if (it == -1) width() - 1 - x else it + 1 }
    return topVisibleTrees * bottomVisibleTrees * leftVisibleTrees * rightVisibleTrees
  }

  fun maxScenicScore(): Int {
    var maxScore = 0
    for (y in 0 until height()) {
      for (x in 0 until width()) {
        val score = treeScenicScore(x, y)
        if (score > maxScore) {
          maxScore = score
        }
      }
    }
    return maxScore
  }
}

fun part1() {
  println("Part 1: ")
  readInput("day_08/sample.txt").lines().let {
    val forrest = Forrest(it)
    println("Sample visible trees: ${forrest.visibleTrees()}")
  }
  readInput("day_08/input_1.txt").lines().let {
    val visibleTrees = Forrest(it).visibleTrees()
    println("Number of visible trees: $visibleTrees")
    assert(visibleTrees == 1695)
  }
}

fun part2() {
  println("Part 2: ")
  readInput("day_08/sample.txt").lines().let {
    val forrest = Forrest(it)
    println("Sample max scenic score: ${forrest.maxScenicScore()}")
  }
  readInput("day_08/input_1.txt").lines().let {
    val maxScenicScore = Forrest(it).maxScenicScore()
    println("Max scenic score: $maxScenicScore")
    assert(maxScenicScore == 287040)
  }
}

fun main() {
  println("Day 8!")
  part1()
  part2()
}
