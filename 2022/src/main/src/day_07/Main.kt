package day_07

import common.readInput

// enum whether it is a file or directory
enum class Type {
    FILE,
    DIRECTORY
}

// a tree node class
class Node(val name: String, val type: Type, val parent:Node? = null, private val size: Int = 0) {
  var children: MutableList<Node> = mutableListOf()

  fun size(): Int {
    return if (type == Type.FILE) size else children.map { it.size() }.sum()
  }
}

// a tree class
class Tree {
  var root: Node = Node("root", type = Type.DIRECTORY)
  var cursor: Node = root;

  // change directory
  fun changeDirectory(path: String) {
    if (path == "/") {
      cursor = root
      return
    }
    if (path == "..") {
      cursor = cursor.parent!!
      return
    }
    if (!path.contains("/")) {
      cursor = cursor.children.find { it.name == path }!!
      return
    }
    throw NotImplementedError("not implemented yet")
  }

  // add file
  fun addFile(path: String, size: Int) {
    if (path.contains("/")) {
      throw NotImplementedError("not implemented yet")
    }
    cursor.children.add(Node(path, Type.FILE, cursor, size))
  }

  // add directory
  fun addDirectory(path: String) {
    if (path.contains("/")) {
      throw NotImplementedError("not implemented yet")
    }
    cursor.children.add(Node(path, Type.DIRECTORY, cursor))
  }

  // Traverse the tree and apply a function to each node accumulating the results.
  fun <T> fold(initial: T, operation: (acc: T, node: Node) -> T): T {
    fun foldRec(acc: T, node: Node): T {
      val newAcc = operation(acc, node)
      return node.children.fold(newAcc, ::foldRec)
    }
    return foldRec(initial, root)
  }

  fun print() {
    fun printRec(node: Node, indent: String) {
      println("$indent${node.name} ${if (node == cursor) "<--" else ""}")
      node.children.forEach { printRec(it, "$indent  ") }
    }
    printRec(root, "")
  }

  fun size(): Int {
    return root.size()
  }
}

fun parseTerminal(lines: List<String>): Tree {
  val tree = Tree()
  for (line in lines) {
    if (line.startsWith("$ ")) {
      line.substring(2).split(" ").filter { it.isNotEmpty() }.let {
        when (it[0]) {
          "cd" -> tree.changeDirectory(it[1])
          "ls" -> {}
        }
      }
    } else if (line.startsWith("dir ")) {
      line.substring(4).trim().let {
        tree.addDirectory(it)
      }
    } else {
      line.split(" ").filter { it.isNotEmpty() }.let {
        tree.addFile(it[1], it[0].toInt())
      }
    }
  }
  return tree
}

fun sumDirectoriesWithTotalSizeNOrLess(tree: Tree, n: Int): Int {
  return tree.fold(0) { acc, node ->
    if (node.type == Type.DIRECTORY && node.size() <= n) acc + node.size() else acc
  }
}

fun part1() {
  println("Part 1: ")
  readInput("day_07/input_1.txt").lines().let {
    val tree = parseTerminal(it)
    sumDirectoriesWithTotalSizeNOrLess(tree, 100000).let {
      println("Sum of total sizes of directories with total size less than 100000: $it")
      assert(it == 1454188)
    }
  }
}

fun findSizeOfSmallestDirectoryToFreeUpSpace(tree: Tree, diskSize: Int, requiredSize: Int): Int {
  val availableSpace = diskSize - tree.size()
  val minimumSpaceToFree = requiredSize - availableSpace
  return tree.fold(Int.MAX_VALUE) { acc, node ->
    if (node.type == Type.DIRECTORY && node.size() >= minimumSpaceToFree) minOf(acc, node.size()) else acc
  }
}

fun part2() {
  println("Part 2: ")
  readInput("day_07/input_1.txt").lines().let {
    val tree = parseTerminal(it)
    findSizeOfSmallestDirectoryToFreeUpSpace(tree, 70000000, 30000000).let {
      println("Size of smallest directory to free up 30000000 bytes: $it")
      assert(it == 4183246)
    }
  }
}

fun main() {
  println("Day 07")
  part1()
  part2()
}
