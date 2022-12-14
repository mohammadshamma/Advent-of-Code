package day_14

import common.readInput

class PointIterator(private val start: Point, private val endInclusive: Point): Iterator<Point> {
  private var current = start
  private var next = true
  override fun hasNext(): Boolean {
    val result = next
    next = current != endInclusive
    return result
  }

  override fun next(): Point {
    val result = current
    current = when {
      current.x == endInclusive.x -> when {
        current.y < endInclusive.y -> Point(current.x, current.y + 1)
        else -> Point(current.x, current.y - 1)
      }
      current.y == endInclusive.y -> when {
        current.x < endInclusive.x -> Point(current.x + 1, current.y)
        else -> Point(current.x - 1, current.y)
      }
      else -> throw IllegalStateException("Current point is not on the same line as endInclusive")
    }
    return result
  }
}

class PointRange(override val start: Point, override val endInclusive: Point): ClosedRange<Point>, Iterable<Point> {
  override fun iterator(): Iterator<Point> {
    return PointIterator(start, endInclusive)
  }
}

class Point(val x: Int, val y: Int): Comparable<Point> {

  fun up(): Point {
    return Point(x, y - 1)
  }

  fun down(): Point {
    return Point(x, y + 1)
  }

  fun left(): Point {
    return Point(x - 1, y)
  }

  fun right(): Point {
    return Point(x + 1, y)
  }

  override fun toString(): String {
    return "($x, $y)"
  }

  override fun compareTo(other: Point): Int {
    return if (y == other.y) x.compareTo(other.x) else y.compareTo(other.y)
  }

  operator fun rangeTo(other: Point): PointRange {
    return PointRange(this, other)
  }

  override fun equals(other: Any?): Boolean {
    if (this === other) return true
    if (javaClass != other?.javaClass) return false

    other as Point

    if (x != other.x) return false
    if (y != other.y) return false

    return true
  }

  override fun hashCode(): Int {
    var result = x
    result = 31 * result + y
    return result
  }
}

class Cave(private val listOfRockPaths: List<List<Point>>) {

  private var caveMap: MutableMap<Point, Char> = mutableMapOf()
  private val minX = listOfRockPaths.map { it.minBy { p-> p.x }.x }.min()
  private val maxX = listOfRockPaths.map { it.maxBy { p-> p.x }.x }.max()
  private val minY = listOfRockPaths.map { it.minBy { p-> p.y }.y }.min()
  private val maxY = listOfRockPaths.map { it.maxBy { p-> p.y }.y }.max()

  init {
    for (rockPath in listOfRockPaths) {
      for (i in 0 .. rockPath.size - 2) {
        for (point in rockPath[i] .. rockPath[i + 1]) {
          caveMap[point] = '#'
        }
      }
    }
  }

  fun printCave() {
    val minX = caveMap.keys.minBy { it.x }.x
    val maxX = caveMap.keys.maxBy { it.x }.x
    for (y in 0 .. maxY + 1) {
      for (x in minX .. maxX) {
        print(caveMap[Point(x, y)] ?: '.')
      }
      println()
    }
    for (x in minX .. maxX) {
      print('#')
    }
    println()
  }

  fun dropSandUntilDrop(start: Point = Point(500, 0)) {
    while(dropSandlet(start)) {}
  }

  fun dropSandUntilFull(start: Point = Point(500, 0)) {
    while(dropSandlet(start, floorExists = true)) {}
  }

  fun countSandlets(): Int {
    return caveMap.values.count { it == 'o' }
  }

  private fun dropSandlet(start: Point, floorExists: Boolean = false): Boolean {
    if (caveMap.containsKey(start)) {
      return false
    }
    var current = start
    while (true) {
      // if there is no ground below, fall
      if (!caveMap.containsKey(current.down())) {
        current = current.down()
      } else if (!caveMap.containsKey(current.left().down())) {
        current = current.left().down()
      } else if (!caveMap.containsKey(current.right().down())) {
        current = current.right().down()
      } else {
        caveMap[current] = 'o'
        return true
      }
      if (floorExists) {
        if (current.y == maxY + 1) {
          caveMap[current] = 'o'
          return true
        }
      } else {
        if (current.y > maxY) {
          return false
        }
      }
    }
  }

  fun printStats() {
    // print minimum and maximum x and y, and size of space
    println("minX: $minX, maxX: $maxX, minY: $minY, maxY: $maxY")
    println("Size of space: ${maxX - minX + 1} x ${maxY - minY + 1} = ${(maxX - minX + 1) * (maxY - minY + 1)}")
  }

  companion object {
    fun fromString(input: String): Cave {
      val listOfRockPaths = input.lines().map { line ->
        line.split(" -> ").map { it.split(",") }.map { Point(it[0].toInt(), it[1].toInt()) }
      }
      return Cave(listOfRockPaths)
    }
  }
}

fun solvePart1(inputPath: String): Int {
  return Cave.fromString(readInput(inputPath)).let {
//    it.printCave()
    it.dropSandUntilDrop()
//    it.printCave()
    it.countSandlets()
  }
}

fun part1() {
  println("Part 1")
  solvePart1("day_14/sample.txt").let {
    println("Sample count of sandlets: $it")
    assert(it == 24)
  }
  solvePart1("day_14/input.txt").let {
    println("Input count of sandlets: $it")
    assert(it == 838)
  }
}

fun solvePart2(inputPath: String): Int {
  return Cave.fromString(readInput(inputPath)).let {
    it.dropSandUntilFull()
//    it.printCave()
    it.countSandlets()
  }
}

fun part2() {
  println("Part 2")
  solvePart2("day_14/sample.txt").let {
    println("Sample count of sandlets: $it")
    assert(it == 93)
  }
  solvePart2("day_14/input.txt").let {
    println("Input count of sandlets: $it")
    assert(it == 27539)
  }
}

fun main () {
  println("Day 14")
  part1()
  part2()
}
