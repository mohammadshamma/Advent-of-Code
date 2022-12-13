package day_13

import common.readInput
import java.lang.Integer.max

interface JsonValue : Comparable<JsonValue> {
  fun equals(other: JsonValue): Boolean

  override operator fun compareTo(other: JsonValue): Int

  companion object {
    fun parse(input: String): JsonValue {
      val trimmed = input.trim()
      return if (trimmed.startsWith("[")) {
        var list = mutableListOf<JsonValue>()
        if (trimmed.length > 2) {
          var tokenBeginning = 1
          var depth = 0
          for (i in  1 until trimmed.length - 1) {
            when (trimmed[i]) {
              '[' -> depth++
              ']' -> depth--
              ',' -> if (depth == 0) {
                list.add(parse(trimmed.substring(tokenBeginning, i)))
                tokenBeginning = i + 1
              }
            }
          }
          if (tokenBeginning < trimmed.length - 1) {
            list.add(parse(trimmed.substring(tokenBeginning, trimmed.length - 1)))
          }
        }
        JsonList(list)
      } else {
        JsonInteger.parse(trimmed)
      }
    }
  }
}

class JsonInteger(val value: Int) : JsonValue {
  override fun equals(other: JsonValue): Boolean {
    if (other is JsonInteger) {
      return value == other.value
    }
    return false
  }

  override fun hashCode(): Int {
    return value
  }

  override fun compareTo(other: JsonValue): Int {
    if (other is JsonInteger) {
      return value.compareTo(other.value)
    } else if (other is JsonList) {
      val newValue = JsonList(listOf(this))
      return newValue.compareTo(other)
    }
    throw IllegalArgumentException("Cannot compare JsonInteger to $other")
  }

  override fun toString(): String = value.toString()

  companion object {
    fun parse(input: String): JsonInteger {
      return JsonInteger(input.toInt())
    }
  }
}

class JsonList(val list: List<JsonValue>): JsonValue {
  override fun equals(other: JsonValue): Boolean {
    if (other is JsonList) {
      return list == other.list
    }
    return false
  }

  override fun hashCode(): Int {
    return list.hashCode()
  }

  override fun compareTo(other: JsonValue): Int {
    if (other is JsonList) {
      for (i in 0 until max(list.size, other.list.size)) {
        if (i == list.size) {
          return -1
        } else if (i == other.list.size) {
          return 1
        }
        val cmp = list[i].compareTo(other.list[i])
        if (cmp != 0) {
          return cmp
        }
      }
      return 0
    } else if (other is JsonInteger) {
      val newOther = JsonList(listOf(other))
      return compareTo(newOther)
    }
    throw IllegalArgumentException("Cannot compare JsonList to $other")
  }

  override fun toString(): String {
    return list.joinToString(", ", "[", "]")
  }
}

fun solvePart1(inputPath: String): Int {
  val jsonPairs = readInput(inputPath).lines().filter { it.isNotBlank() }.chunked(2)
  var indicesWithRightOrder = mutableListOf<Int>()
  for (i in jsonPairs.indices) {
    val jsonPair = jsonPairs[i]
    val json1 = JsonValue.parse(jsonPair[0])
    val json2 = JsonValue.parse(jsonPair[1])
    if (json1 < json2) {
      indicesWithRightOrder.add(i + 1)
    }
  }
  println("Right ordered indices: $indicesWithRightOrder")
  return indicesWithRightOrder.sum()
}

fun part1() {
  println("Part 1")
  solvePart1("day_13/sample.txt").let { result ->
    println("Sample: $result")
    assert(result == 13)
  }
  solvePart1("day_13/input.txt").let { result ->
    println("Result: $result")
    assert(result == 6656)
  }
}

fun solvePart2(inputPath: String): Int {
  val jsonValues = readInput(inputPath).lines().filter { it.isNotBlank() }.map { JsonValue.parse(it) }
  val distressSignalOne = JsonValue.parse("[[2]]")
  val distressSignalTwo = JsonValue.parse("[[6]]")
  val distressSignals = listOf<JsonValue>(distressSignalOne, distressSignalTwo)
  val jsonValuesAndDistressSignals = jsonValues + distressSignals
  val jsonValuesAndDistressSignalsSorted = jsonValuesAndDistressSignals.sorted()
  return (jsonValuesAndDistressSignalsSorted.indexOf(distressSignalOne) + 1) * (jsonValuesAndDistressSignalsSorted.indexOf(distressSignalTwo) + 1)
}

fun part2() {
  println("Part 2")
  solvePart2("day_13/sample.txt").let { result ->
    println("Sample: $result")
    assert(result == 140)
  }
  solvePart2("day_13/input.txt").let { result ->
    println("Result: $result")
    assert(result == 19716)
  }
}

fun main () {
  println("Day 13")
  part1()
  part2()
}
