package day_01

val JAVA_CLASS = {}.javaClass
fun main() {
  println("Hello Day 1!")
  part1()
  part2()
}

fun getCaloriesPerElf(): List<Int> {
  val elvesCalories = mutableListOf<Int>()
  var currentElfCalories = 0
  JAVA_CLASS.getResourceAsStream("input_1.txt")?.bufferedReader()?.forEachLine {
    if (it != "") {
      currentElfCalories += it.toInt()
    } else {
      elvesCalories.add(currentElfCalories)
      currentElfCalories = 0
    }
  }
  elvesCalories.add(currentElfCalories)
  return elvesCalories
}

fun part1() {
  val elvesCalories = getCaloriesPerElf()
  elvesCalories.indices.maxBy { elvesCalories[it] }.let {
    println("Part 1: Elf ${it} has the max calories: ${elvesCalories[it]}")
    // Elf 171 has the max calories: 70509
    assert(it == 171)
    assert(elvesCalories[it] == 70509)
  }
}

fun part2() {
  val elvesCalories = getCaloriesPerElf()
  elvesCalories.sortedDescending().take(3).sum().let {
    println("Part 2: The top 3 elves have a total of $it calories")
    // The top 3 elves have a total of 208567 calories
    assert(it == 208567)
  }
}
