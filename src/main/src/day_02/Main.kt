package day_02

val JAVA_CLASS = {}.javaClass

enum class Move (val value: Int) {
  Rock(1),
  Paper(2),
  Scissors(3)
}

enum class TheirMove(val move: Move) {
  A(Move.Rock),
  B(Move.Paper),
  C(Move.Scissors)
}

enum class MyMove(val move: Move) {
  X(Move.Rock),
  Y(Move.Paper),
  Z(Move.Scissors)
}

enum class RoundResult {
  X, // Lose
  Y, // Draw
  Z  // Win
}

fun calculateHeadToHeadPoints(theirMove: TheirMove, myMove: MyMove): Int {
  val myMove = myMove.move
  val theirMove = theirMove.move
  if (myMove == theirMove) {
    return 3
  } else if (myMove == Move.Rock && theirMove == Move.Scissors) {
    return 6
  } else if (myMove == Move.Paper && theirMove == Move.Rock) {
    return 6
  } else if (myMove == Move.Scissors && theirMove == Move.Paper) {
    return 6
  } else {
    return 0
  }
}

fun calculateRoundResult(theirMove: TheirMove, myMove: MyMove): Int {

  val headToHeadPoints = calculateHeadToHeadPoints(theirMove, myMove)
  val myMovePoints = myMove.move.value
  return headToHeadPoints + myMovePoints
}

fun calculateNextMove(theirMove: TheirMove, desiredRountResult: RoundResult): Move {
  val theirMove = theirMove.move
  when (desiredRountResult) {
    RoundResult.X -> {  // Lose
      return when (theirMove) {
        Move.Paper -> Move.Rock
        Move.Rock -> Move.Scissors
        Move.Scissors -> Move.Paper
      }
    }
    RoundResult.Y -> {  // Draw
      return theirMove
    }
    RoundResult.Z -> {  // Win
      return when (theirMove) {
        Move.Paper -> Move.Scissors
        Move.Rock -> Move.Paper
        Move.Scissors -> Move.Rock
      }
    }
  }
}

// My eyes are bleeding. I'm sorry.
fun convertToMyMove(move: Move): MyMove {
  return when (move) {
    Move.Rock -> MyMove.X
    Move.Paper -> MyMove.Y
    Move.Scissors -> MyMove.Z
  }
}

fun main() {
  println("Hello Day 2!")
  part1()
  part2()
}

fun part1() {
  var totalPoints = 0
  JAVA_CLASS.getResourceAsStream("input_1.txt")?.bufferedReader()?.forEachLine {
    val moves = it.split(" ")
    assert(moves.size == 2)
    val theirMove = TheirMove.valueOf(moves[0])
    val myMove = MyMove.valueOf(moves[1])
    val roundResult = calculateRoundResult(theirMove, myMove)
    totalPoints += roundResult
  }
  println("Total points: $totalPoints")
  assert(totalPoints == 13675)
}

fun part2() {
  var totalPoints = 0;
  JAVA_CLASS.getResourceAsStream("input_1.txt")?.bufferedReader()?.forEachLine {
    val moves = it.split(" ")
    assert(moves.size == 2)
    val theirMove = TheirMove.valueOf(moves[0])
    val desiredResult = RoundResult.valueOf(moves[1])
    val myMove = calculateNextMove(theirMove, desiredResult)
    val roundResult = calculateRoundResult(theirMove, convertToMyMove(myMove))
    totalPoints += roundResult
  }
  println("Total points: $totalPoints")
  assert(totalPoints == 14184)
}
