package day_10

import common.readInput

class SimpleCpu {
  var registerX = 1
  var cycle = 1
  val registerXValuesPerCycle = mutableListOf<Int>()

  fun execute(instruction: String) {
    val args = instruction.split(" ")
    when (args[0]) {
      "addx" -> {
        registerXValuesPerCycle.add(registerX)
        registerXValuesPerCycle.add(registerX)
        cycle += 2
        registerX += args[1].toInt()
      }
      "noop" -> {
        registerXValuesPerCycle.add(registerX)
        cycle += 1
      }
      else -> throw IllegalArgumentException("Unknown instruction: $instruction")
    }
  }

  fun executeAll(instructions: List<String>) {
    instructions.forEach { execute(it) }
  }

  fun getSpriteLocation(cycle: Int): Int {
    return registerXValuesPerCycle[cycle - 1]
  }

  fun getSignalStrength(cycle: Int): Int {
    return registerXValuesPerCycle[cycle - 1] * cycle
  }

  fun getSignalStrengthSum(): Int {
    return listOf(20, 60, 100, 140, 180, 220).sumOf { getSignalStrength(it) }
  }
}

fun getSignalStrengthSum(inputPath: String): Int {
  val cpu = SimpleCpu()
  cpu.executeAll(readInput(inputPath).lines())
  println("Signal strength on 20th cycle: ${cpu.getSignalStrength(20)}")
  return cpu.getSignalStrengthSum()
}

class SimpleCathodeRayTube (private val cpu: SimpleCpu) {
  val ROWS = 6
  val COLS = 40
  val screen = Array(ROWS) { CharArray(COLS) { ' ' } }
  val lines: ArrayList<String> = ArrayList()

  fun draw(): List<String> {
    var cycle = 1
    for (row in 0 until ROWS) {
      for (col in 0 until COLS) {
        val spriteLocation = cpu.getSpriteLocation(cycle)
        when (col) {
            spriteLocation -> {
              screen[row][col] = '#'
            }
            spriteLocation + 1 -> {
              screen[row][col] = '#'
            }
            spriteLocation - 1 -> {
              screen[row][col] = '#'
            }
            else -> {
              screen[row][col] = '.'
            }
        }
        cycle++
      }
      lines.add(screen[row].joinToString(""))
    }
    return lines
  }
}

fun part1() {
  println("Part 1:")
  getSignalStrengthSum("day_10/sample.txt").let {
    println("Sample sum of strength: $it")
    assert(it == 13140)
  }
  getSignalStrengthSum("day_10/input_1.txt").let {
    println("Input sum of strength: $it")
    assert(it == 12880)
  }
}

fun getScreenDrawing(inputPath: String): List<String> {
  val cpu = SimpleCpu()
  cpu.executeAll(readInput(inputPath).lines())
  val screen = SimpleCathodeRayTube(cpu)
  return screen.draw()
}

fun part2() {
  println("Part 2:")
  getScreenDrawing("day_10/sample.txt").let {
    println("Sample screen drawing:")
    it.forEach { println(it) }
  }
  getScreenDrawing("day_10/input_1.txt").let {
    println("Input screen drawing:")
    it.forEach { println(it) }
    val expected = listOf(
        "####..##....##..##..###....##.###..####.",
        "#....#..#....#.#..#.#..#....#.#..#.#....",
        "###..#.......#.#..#.#..#....#.#..#.###..",
        "#....#.......#.####.###.....#.###..#....",
        "#....#..#.#..#.#..#.#....#..#.#.#..#....",
        "#.....##...##..#..#.#.....##..#..#.####."
    )
    assert(it == expected)
  }
}
fun main() {
  println("Day 10!!")
  part1()
  part2()
}
