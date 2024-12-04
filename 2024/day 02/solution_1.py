# Gemini conversation: https://g.co/gemini/share/33ac0ebd54ce

def is_safe_report(report):
  """
  Checks if a report meets the safety criteria.

  Args:
    report: A list of integers representing the levels in the report.

  Returns:
    True if the report is safe, False otherwise.
  """
  if len(report) < 2:  # A report with less than 2 levels is considered safe
    return True

  increasing = report[1] > report[0]  # Determine if the trend is increasing or decreasing

  for i in range(1, len(report)):
    if increasing and report[i] <= report[i - 1]:
      return False  # Not increasing
    if not increasing and report[i] >= report[i - 1]:
      return False  # Not decreasing
    if abs(report[i] - report[i - 1]) > 3:
      return False  # Difference exceeds limit

  return True


def count_safe_reports(filename):
  """
  Counts the number of safe reports in a file.

  Args:
    filename: The name of the file containing the reports.

  Returns:
    The number of safe reports.
  """
  safe_count = 0
  with open(filename, 'r') as file:
    for line in file:
      levels = [int(level) for level in line.strip().split()]
      if is_safe_report(levels):
        safe_count += 1
  return safe_count


if __name__ == "__main__":
  filename = "input_1.txt"
  safe_reports = count_safe_reports(filename)
  print(f"There are {safe_reports} safe reports.")
