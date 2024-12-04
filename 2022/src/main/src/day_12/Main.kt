package day_12

import common.readInput

interface Graph<K> {
  fun getAdjacentNodes(node: K): List<K>
}

class Position (val x: Int, val y: Int) {
  override fun equals(other: Any?): Boolean {
    if (other is Position) {
      return x == other.x && y == other.y
    }
    return false
  }

  override fun hashCode(): Int {
    return x * 31 + y
  }

  override fun toString(): String {
    return "($x, $y)"
  }
}

class TwoDimensionalMap(private val map: List<List<Char>>, private val part2: Boolean = false) : Graph<Position> {
  private val width = map[0].size
  private val height = map.size
  private val initialPosition = findOnly('S')
  private val endPosition = findOnly('E')

  fun getInitialPosition() = initialPosition
  fun getEndPosition() = endPosition

  fun getCharAt(position: Position) = map[position.y][position.x]

  private fun findOnly(char: Char): Position {
    // find the only position of the given character
    var position: Position? = null
    for (y in 0 until height) {
      for (x in 0 until width) {
        if (map[y][x].equals(char, ignoreCase = false)) {
          if (position != null) {
            throw IllegalArgumentException("There are more than one '$char' in the map")
          }
          position = Position(x=x, y=y)
        }
      }
    }
    return position ?: throw IllegalArgumentException("There is no '$char' in the map")
  }

  private fun getCharacterValue(character: Char): Int {
    return character.let { if (it == 'S') 'a'.code else if (it == 'E') 'z'.code else it.code }
  }
  private fun characterIsAtMostOneStepAbove(from: Char, to: Char): Boolean {
    val fromValue = getCharacterValue(from)
    val toValue = getCharacterValue(to)
    return when (part2) {
      false -> return fromValue + 1 >= toValue
      true -> return toValue + 1 >= fromValue
    }
  }

  override fun getAdjacentNodes(node: Position): List<Position> {

    // Check adjacent nodes and return only the ones that are at most one value above
    val adjacentNodes = mutableListOf<Position>()
    // top
    if (node.y > 0 && characterIsAtMostOneStepAbove(map[node.y][node.x], map[node.y - 1][node.x])) {
      adjacentNodes.add(Position(x=node.x, y=node.y - 1))
    }
    // bottom
    if (node.y < height - 1 && characterIsAtMostOneStepAbove(map[node.y][node.x], map[node.y + 1][node.x])) {
      adjacentNodes.add(Position(x=node.x, y=node.y + 1))
    }
    // left
    if (node.x > 0 && characterIsAtMostOneStepAbove(map[node.y][node.x], map[node.y][node.x - 1])) {
      adjacentNodes.add(Position(x=node.x - 1, y=node.y))
    }
    // right
    if (node.x < width - 1 && characterIsAtMostOneStepAbove(map[node.y][node.x], map[node.y][node.x + 1])) {
      adjacentNodes.add(Position(x=node.x + 1, y=node.y))
    }
    return adjacentNodes
  }

  // static function to parse map from list of strings
  companion object {
    fun parseMap(map: List<String>, part2: Boolean = false): TwoDimensionalMap {
      return TwoDimensionalMap(map.map { it.toList() }, part2=part2)
    }
  }
}

// Breadth-first search a graph from a given start node to a given end node
fun <K> breadthFirstSearch(graph: Graph<K>, start: K, endCondition: (K) -> Boolean): List<K> {
  val queue = mutableListOf<K>()
  val visited = mutableSetOf<K>()
  val referrer = mutableMapOf<K, K>()
  queue.add(start)
  while (queue.isNotEmpty()) {
    val node = queue.removeAt(0)
    if (endCondition(node)) {
      // we found the end node, return the path
      val path = mutableListOf<K>()
      var current = node
      while (current != start) {
        path.add(current)
        current = referrer[current]!!
      }
      path.add(start)
      return path.reversed()
    }
    if (node in visited) {
      continue
    }
    visited.add(node)
    for (adjacent in graph.getAdjacentNodes(node)) {
      if (adjacent !in referrer) {
        referrer[adjacent] = node
        queue.add(adjacent)
      }
    }
  }
  return emptyList()
}

fun solvePart1(inputPath: String): Int {
  return TwoDimensionalMap.parseMap(readInput(inputPath).lines()).let { graph ->
    println("Results for $inputPath")
    println(" Start: ${graph.getInitialPosition()}")
    println(" End: ${graph.getEndPosition()}")
    val path = breadthFirstSearch(graph, graph.getInitialPosition()) { it == graph.getEndPosition() }
    println(" Sample path: ${path.joinToString(" -> ")}")
    println(" Path size ${path.size - 1}")
    path.size - 1
  }
}

fun part1() {
  println("Part 1:")
  assert(solvePart1("day_12/sample.txt") == 31)
  assert(solvePart1("day_12/input.txt") == 391)
}

fun solvePart2(inputPath: String): Int {
  return TwoDimensionalMap.parseMap(readInput(inputPath).lines(), part2 = true).let { graph ->
    println("Results for $inputPath")
    println(" End: ${graph.getEndPosition()}")
    val path = breadthFirstSearch(graph, graph.getEndPosition()) {
      graph.getCharAt(it) == 'a'
    }
    println(" Path to closest 'a': ${path.joinToString(" -> ")}")
    println(" Path size ${path.size - 1}")
    path.size - 1
  }
}

fun part2() {
  println("Part 2:")
  assert(solvePart2("day_12/sample.txt") == 29)
  assert(solvePart2("day_12/input.txt") == 386)
}

fun main () {
  println("Day 12")
  part1()
  part2()
}
