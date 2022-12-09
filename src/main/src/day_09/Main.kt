package day_09

import common.readInput
import kotlin.math.abs
import kotlin.math.sign

class Point(val x: Int, val y: Int) {
  fun adjacentOrOverlapping(other: Point): Boolean {
    return abs(y - other.y) <= 1 && abs(x - other.x) <= 1
  }

  fun moveTowards(other: Point): Point {
    return Point(x + (other.x - x).sign, y + (other.y - y).sign)
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
  override fun toString(): String {
    return "($x, $y)"
  }
}

enum class Direction {
  U, D, L, R
}

class Rope {

  var head: Point
  var tail: Point
  var tailTrail = ArrayList<Point>()

  constructor(head:Point, tail:Point) {
    this.head = head
    this.tail = tail
  }

  fun move(direction: Direction) {
    when (direction) {
      Direction.U -> head = Point(head.x, head.y - 1)
      Direction.D -> head = Point(head.x, head.y + 1)
      Direction.L -> head = Point(head.x - 1, head.y)
      Direction.R -> head = Point(head.x + 1, head.y)
    }

    if (!head.adjacentOrOverlapping(tail)) {
      tail = tail.moveTowards(head)
    }
    tailTrail.add(tail)
  }

  fun getUniqueTailTrailPointCount(): Int {
    return tailTrail.toSet().size
  }
}

class MultiPointRope(val ropeSize:Int) {
  val points = ArrayList<Point>()
  var tailTrail = ArrayList<Point>()

  init {
    for (i in 0 until ropeSize) {
      points.add(Point(0, 0))
    }
  }

  fun move(direction: Direction) {
    var head = points[0]
    when (direction) {
      Direction.U -> head = Point(head.x, head.y - 1)
      Direction.D -> head = Point(head.x, head.y + 1)
      Direction.L -> head = Point(head.x - 1, head.y)
      Direction.R -> head = Point(head.x + 1, head.y)
    }
    points[0] = head
    for (i in 1 until ropeSize) {
      if (!points[i-1].adjacentOrOverlapping(points[i])) {
        points[i] = points[i].moveTowards(points[i - 1])
      }
    }
    tailTrail.add(points.last())
  }

  fun executeMoves(moves: List<String>) {
    moves.forEach { move ->
      val parts = move.split(" ")
      assert(parts.size == 2)
      for (i in 0 until parts[1].toInt()) {
        move(Direction.valueOf(parts[0]))
      }
    }
  }

  fun getUniqueTailTrailPointCount(): Int {
    return tailTrail.toSet().size
  }
}

fun executeMovesAndGetUniqueTailTrailPointsCount(filePath: String): Int {
  val moves = readInput(filePath).lines()
  val rope = Rope(Point(0, 0), Point(0, 0))
  moves.forEach { move ->
    val parts = move.split(" ")
    assert(parts.size == 2)
    for (i in 0 until parts[1].toInt()) {
      rope.move(Direction.valueOf(parts[0]))
    }
  }
  return rope.getUniqueTailTrailPointCount()
}

fun solvePart2(filePath: String): Int {
  val moves = readInput(filePath).lines()
  val rope = MultiPointRope(10)
  rope.executeMoves(moves)
  return rope.getUniqueTailTrailPointCount()
}

fun part1() {
  println("Part 1:")
  println("Unique sample tail trail points count: ${executeMovesAndGetUniqueTailTrailPointsCount("day_09/sample.txt")}")
  executeMovesAndGetUniqueTailTrailPointsCount("day_09/input_1.txt").let {
    println("Unique tail trail points count: $it")
    assert(it == 5695)
  }
}

fun part2() {
  println("Part 2:")
  solvePart2("day_09/sample.txt").let {
    println("Sample unique tail trail points count: $it")
  }
  solvePart2("day_09/input_1.txt").let {
    println("Unique tail trail points count: $it")
    assert(it == 2434)
  }
}

fun main () {
  println("Day 9")
  part1()
  part2()
}
