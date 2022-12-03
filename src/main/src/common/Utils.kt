package common
fun readInput(inputFileAbsolutePath: String):String {
  return {}.javaClass.classLoader.getResource(inputFileAbsolutePath)!!.readText()
}
