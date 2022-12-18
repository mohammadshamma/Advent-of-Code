package day_15

import common.readInput
import java.math.BigInteger
import java.text.DecimalFormat
import kotlin.math.pow

class Position(val x: Int, val y: Int) {
  fun manhattanDistanceTo(other: Position): Int {
    return kotlin.math.abs(x - other.x) + kotlin.math.abs(y - other.y)
  }

  fun withinRangeOf(other: Position, distance: Int): Boolean {
    return manhattanDistanceTo(other) <= distance
  }

  fun inSquare(min: Int, max: Int): Boolean {
    return x in min..max && y in min..max
  }

  fun tuningFrequency(): BigInteger {
    return 4000000.toBigInteger() * x.toBigInteger() + y.toBigInteger()
  }

  override fun toString(): String {
    return "($x, $y)"
  }

  override fun equals(other: Any?): Boolean {
    if (this === other) return true
    if (javaClass != other?.javaClass) return false

    other as Position

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

class SlopedRectangle(val minSum: Int, val maxSum: Int, val minDiff: Int, val maxDiff: Int) {

  fun contains(position: Position): Boolean {
    val sum = position.x + position.y
    val diff = position.x - position.y
    return sum in minSum..maxSum && diff in minDiff..maxDiff
  }

  fun partiallyOverlaps(other: SlopedRectangle): Boolean {
    return minSum <= other.maxSum && maxSum >= other.minSum && minDiff <= other.maxDiff && maxDiff >= other.minDiff
  }

  fun contains(other: SlopedRectangle): Boolean {
    return minSum <= other.minSum && maxSum >= other.maxSum && minDiff <= other.minDiff && maxDiff >= other.maxDiff
  }

  fun subtract(other: SlopedRectangle): List<SlopedRectangle> {
    val result = mutableListOf<SlopedRectangle>()
    // Calculate the upper left chunk
    if (minSum < other.minSum) {
      result.add(SlopedRectangle(minSum, other.minSum - 1, minDiff, maxDiff))
    }
    if (maxSum > other.maxSum) {
      result.add(SlopedRectangle(other.maxSum + 1, maxSum, minDiff, maxDiff))
    }
    if (minDiff < other.minDiff) {
      result.add(SlopedRectangle(minSum, maxSum, minDiff, other.minDiff - 1))
    }
    if (maxDiff > other.maxDiff) {
      result.add(SlopedRectangle(minSum, maxSum, other.maxDiff + 1, maxDiff))
    }
    return result
  }

  fun isSinglePoint(): Boolean {
    return minSum == maxSum && minDiff == maxDiff && (minSum - minDiff) % 2 == 0
  }

  fun getSinglePoint(): Position {
    assert(isSinglePoint())
    return Position((minSum + minDiff) / 2, (minSum - minDiff) / 2)
  }

  fun getLeftMostPositions(): List<Position> {
    return if ((minSum - minDiff) % 2 == 0) {
      listOf(Position((minSum + minDiff) / 2, (minSum - minDiff) / 2))
    } else {
      listOf(
        Position((minSum + minDiff + 1) / 2, (minSum - minDiff) / 2),
        Position((minSum + minDiff + 1) / 2, (minSum - minDiff) / 2 + 1)
      )
    }
  }

  fun getRightMostPositions(): List<Position> {
    return if ((maxSum - maxDiff) % 2 == 0) {
      listOf(Position((maxSum + maxDiff) / 2, (maxSum - maxDiff) / 2))
    } else {
      listOf(
        Position((maxSum + maxDiff) / 2, (maxSum - maxDiff) / 2),
        Position((maxSum + maxDiff) / 2, (maxSum - maxDiff) / 2 + 1)
      )
    }
  }

  fun getTopMostPositions(): List<Position> {
    return if ((minSum + maxDiff) % 2 == 0) {
      listOf(Position((minSum + maxDiff) / 2, (minSum - maxDiff) / 2))
    } else {
      listOf(
        Position((minSum + maxDiff) / 2, (minSum - maxDiff + 1) / 2),
        Position((minSum + maxDiff) / 2 + 1, (minSum - maxDiff + 1) / 2)
      )
    }
  }

  fun getBottomMostPositions(): List<Position> {
    return if ((maxSum + minDiff) % 2 == 0) {
      listOf(Position((maxSum + minDiff) / 2, (maxSum - minDiff) / 2))
    } else {
      listOf(
        Position((maxSum + minDiff) / 2, (maxSum - minDiff) / 2),
        Position((maxSum + minDiff) / 2 + 1, (maxSum - minDiff) / 2)
      )
    }
  }

  fun intersectsWithBox(min: Int, max: Int): Boolean {
    return (
      minSum in min..max &&
        getLeftMostPositions().minOf { it.y } >= min &&
        getTopMostPositions().minOf { it.x } >= min)
      ||
      (
        minSum in (max - min)..2 * (max - min) &&
          getLeftMostPositions().minOf { it.x } <= max &&
          getTopMostPositions().minOf { it.y } <= max
        )
      ||
      (
        maxSum in min..max &&
          getBottomMostPositions().minOf { it.y } >= min &&
          getRightMostPositions().minOf { it.x } >= min
        )
      ||
      (
        maxSum in (max - min)..2 * (max - min) &&
          getBottomMostPositions().minOf { it.x } <= max &&
          getRightMostPositions().minOf { it.y } <= max
      )
      ||
      (
        maxDiff in (min - max)..min &&
          getTopMostPositions().minOf { it.y } <= max &&
          getRightMostPositions().maxOf { it.x } >= min
        )
      ||
      (
        maxDiff in min..(max - min) &&
          getTopMostPositions().maxOf { it.x } <= max &&
          getRightMostPositions().maxOf { it.y } >= min
        )
      ||
      (
        minDiff in (min - max)..min &&
          getLeftMostPositions().minOf { it.y } <= max &&
          getBottomMostPositions().maxOf { it.x } >= min
        )
      ||
      (
        minDiff in min..(max - min) &&
          getLeftMostPositions().minOf { it.x } <= max &&
          getBottomMostPositions().maxOf { it.y } >= min
        )
  }

  // ..............
  // ..............
  // ..x...........
  // .x............
  // .o............
  // ..o...........
  // ..............
  // minSum = 4, minDiff = -3 => minX = 1
  // x - y = -3
  // x + y = 4
  // 2x = 1
  // x = 1/2

  // ..............
  // ..............
  // ..x...........
  // .x............
  // x.............
  // o.............
  // .o............
  // ..o...........
  // x + y = 4
  // x - y = -5
  // 2x = -1
  // x = -1/2


  // ..............
  // ..............
  // ..x...........
  // .#............
  // ..o...........
  // ..............
  // ..............
  // minSum = 4, minDiff = -2 => minX = 1
  // x - y = -2
  // x + y = 4
  // 2x = 2
  // x = 1

  override fun toString(): String {
    return "SlopedRectangle(minSum=$minSum, maxSum=$maxSum, minDiff=$minDiff, maxDiff=$maxDiff)"
  }

  override fun equals(other: Any?): Boolean {
    if (this === other) return true
    if (javaClass != other?.javaClass) return false

    other as SlopedRectangle

    if (minSum != other.minSum) return false
    if (maxSum != other.maxSum) return false
    if (minDiff != other.minDiff) return false
    if (maxDiff != other.maxDiff) return false

    return true
  }

  override fun hashCode(): Int {
    var result = minSum
    result = 31 * result + maxSum
    result = 31 * result + minDiff
    result = 31 * result + maxDiff
    return result
  }

  companion object {
    fun fromSensorPositionAndDistance(centerPosition: Position, distance: Int): SlopedRectangle {
      val minSum = centerPosition.x + centerPosition.y - distance
      val maxSum = centerPosition.x + centerPosition.y + distance
      val minDiff = centerPosition.x - centerPosition.y - distance
      val maxDiff = centerPosition.x - centerPosition.y + distance
      return SlopedRectangle(minSum, maxSum, minDiff, maxDiff)
    }

    fun fromSquareCovered(min: Int, max: Int): SlopedRectangle {
      val minSum = min + min
      val maxSum = max + max
      val minDiff = min - max
      val maxDiff = max - min
      return SlopedRectangle(minSum, maxSum, minDiff, maxDiff)
    }
  }
}

class SensorsBeaconsMap(sensorsAndBeacons: List<Pair<Position, Position>>) {
  private val sensors: Map<Position, Int> =
    sensorsAndBeacons.associate { Pair(it.first, it.first.manhattanDistanceTo(it.second)) }
  private val beacons: Set<Position> = sensorsAndBeacons.map { it.second }.toSet()
  private val maxSensorX: Int = sensors.keys.map { it.x }.max()
  private val maxSensorY: Int = sensors.keys.map { it.y }.max()
  private val maxBeaconX: Int = beacons.map { it.x }.max()
  private val maxBeaconY: Int = beacons.map { it.y }.max()
  private val minSensorX: Int = sensors.keys.map { it.x }.min()
  private val minSensorY: Int = sensors.keys.map { it.y }.min()
  private val minBeaconX: Int = beacons.map { it.x }.min()
  private val minBeaconY: Int = beacons.map { it.y }.min()
  private val maxManhattanDistance: Int = sensors.values.max()!!
  private val maxX: Int = maxOf(maxSensorX, maxBeaconX, maxSensorX + maxManhattanDistance)
  private val maxY: Int = maxOf(maxSensorY, maxBeaconY, maxSensorY + maxManhattanDistance)
  private val minX: Int = minOf(minSensorX, minBeaconX, minSensorX - maxManhattanDistance)
  private val minY: Int = minOf(minSensorY, minBeaconY, minSensorY - maxManhattanDistance)

  fun printMinMaxStats() {
    println("maxX: $maxX, maxY: $maxY")
    println("minX: $minX, minY: $minY")
  }

  fun countPositionsThatCannotContainBeacon(y: Int): Int {
    var count = 0
    for (x in minX..maxX) {
      val position = Position(x, y)
      if (sensors.keys.any {
          it.withinRangeOf(
            position,
            sensors[it]!!
          )
        } && !beacons.contains(position) && !sensors.containsKey(position)) {
        count++
      }
    }
    return count
  }

  fun dumbGetOnlyPositionNotInRangeOfAnySensor(min: Int, max: Int): Position? {
    var result: Position? = null
    val allResults = mutableListOf<Position>()
    for (x in min..max) {
      for (y in min..max) {
        val position = Position(x, y)
        if (sensors.keys.none {
            it.withinRangeOf(
              position,
              sensors[it]!!
            )
          } && !beacons.contains(position) && !sensors.containsKey(position)) {
          result = position
          allResults.add(position)
        }
      }
    }
    println("allResults: $allResults")
    return result
  }

  fun getOnlyPositionNotInRangeOfAnySensor(min: Int, max: Int): Position? {
    val diamond = SlopedRectangle.fromSquareCovered(min, max)
    val rectangles = mutableListOf(diamond)
    sensors.map { SlopedRectangle.fromSensorPositionAndDistance(it.key, it.value) }.forEach {
      val newRectangles = mutableListOf<SlopedRectangle>()
      rectangles.forEachIndexed { index, rectangle ->
        if (rectangle.partiallyOverlaps(it)) {
          val newRectanglesForThisRectangle = rectangle.subtract(it)
          // filter out rectangles that are outside of the range
          newRectanglesForThisRectangle.forEach { newRectangle ->
            if (newRectangle.intersectsWithBox(min, max)) {
              newRectangles.add(newRectangle)
            }
          }
        } else {
          newRectangles.add(rectangle)
        }
      }
      rectangles.clear()
      rectangles.addAll(newRectangles)
    }
    var leftOverRectangles = rectangles.toSet()
    assert(leftOverRectangles.size == 1)
    return leftOverRectangles.first().getSinglePoint()
  }

  fun printRectangles(min: Int, max: Int, rectangles: List<SlopedRectangle>) {
    println("printing rectangles (${rectangles.size}): $rectangles")
    for (y in 1 downTo 0) {
      print("    ")
      for (x in min..max) {
        // print the yth digit of x
        val digit = (x / 10.0.pow(y)) % 10;
        // cast the digit to an int and print it
        print(digit.toInt())
      }
      println()
    }
    println()
    for (y in min..max) {
      print("${DecimalFormat("00").format(y)}: ")
      for (x in min..max) {
        val position = Position(x, y)
        val char = when {
          rectangles.any { it.contains(position) } -> 'o'
          else -> 'X'
        }
        print(char)
      }
      println()
    }
  }

  companion object {
    fun fromString(input: String): SensorsBeaconsMap {
      val sensorsAndBeacons = input.lines().map { line ->
        // Sample line: Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        val stringParts = line.split(":")
        assert(stringParts.size == 2)
        val sensorString = stringParts[0]
        val beaconString = stringParts[1]
        val sensorX = sensorString.substringAfter("x=").substringBefore(",").toInt()
        val sensorY = sensorString.substringAfter("y=").toInt()
        val beaconX = beaconString.substringAfter("x=").substringBefore(",").toInt()
        val beaconY = beaconString.substringAfter("y=").toInt()
        Pair(Position(sensorX, sensorY), Position(beaconX, beaconY))
      }
      return SensorsBeaconsMap(sensorsAndBeacons)
    }
  }
}

fun solvePart1(inputPath: String, rowToCheck: Int): Int {
  return SensorsBeaconsMap.fromString(readInput(inputPath)).countPositionsThatCannotContainBeacon(rowToCheck)
}

fun part1() {
  println("Part 1")
  solvePart1("day_15/sample.txt", 10).let {
    println("Sample positions that cannot contain beacons: $it")
    assert(it == 26)
  }
  solvePart1("day_15/input.txt", 2000000).let {
    println("Input positions that cannot contain beacons: $it")
    assert(it == 5688618)
  }
}

fun solvePart2(inputPath: String, min: Int, max: Int): BigInteger {
  return SensorsBeaconsMap.fromString(readInput(inputPath)).let { it ->
    val position = it.getOnlyPositionNotInRangeOfAnySensor(min, max)
    return position!!.tuningFrequency()
  }
}

fun part2() {
  println("Part 2")
  solvePart2("day_15/sample.txt", 0, 20).let {
    println("Sample tuning frequency: $it")
    assert(it == BigInteger("56000011"))
  }
  solvePart2("day_15/input.txt", 0, 4000000).let {
    println("Input tuning frequency: $it")
    assert(it == BigInteger("12625383204261"))
  }
}

fun main() {
  println("Day 15")
  part1()
  part2()
}
