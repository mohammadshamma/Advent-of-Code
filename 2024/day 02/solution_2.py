# Gemini conversation: https://g.co/gemini/share/d4909ed1a234

def is_safe_report(report):
  """
  Checks if a report meets the safety criteria (with no level removal).

  Args:
    report: A list of integers representing the levels in the report.

  Returns:
    True if the report is safe, False otherwise.
  """
  if len(report) < 2:
    return True

  increasing = report[1] > report[0]

  for i in range(1, len(report)):
    if increasing and report[i] <= report[i - 1]:
      return False
    if not increasing and report[i] >= report[i - 1]:
      return False
    if abs(report[i] - report[i - 1]) > 3:
      return False

  return True


def is_safe_with_dampener(report):
  """
  Checks if a report is safe, potentially using the Problem Dampener.

  Args:
    report: A list of integers representing the levels in the report.

  Returns:
    True if the report is safe (with or without the dampener),
    False otherwise.
  """
  if is_safe_report(report):
    return True

  # Try removing each level and check if the report becomes safe
  for i in range(len(report)):
    modified_report = report[:i] + report[i+1:]
    if is_safe_report(modified_report):
      return True

  return False


def count_safe_reports(filename):
  """
  Counts the number of safe reports in a file, considering the dampener.

  Args:
    filename: The name of the file containing the reports.

  Returns:
    The number of safe reports.
  """
  safe_count = 0
  with open(filename, 'r') as file:
    for line in file:
      levels = [int(level) for level in line.strip().split()]
      if is_safe_with_dampener(levels):
        safe_count += 1
  return safe_count


if __name__ == "__main__":
  filename = "input_1.txt"
  safe_reports = count_safe_reports(filename)
  print(f"There are {safe_reports} safe reports (with the dampener).")
