#!/usr/bin/env python3 

from collections import defaultdict
import numpy as np
import re


IDENTITY = np.identity(3, dtype=int)
RX = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=int)  # One 90' rotation around x axis.
RY = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]], dtype=int)
RZ = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=int)

ALL_POSSIBLE_ROTATIONS = [
  # Positive Z pointing to the top possibilities.
  IDENTITY,
  RZ,
  RZ.dot(RZ),
  RZ.dot(RZ).dot(RZ),
  # Negative Z pointing to the top possibilities.
  RX.dot(RX),
  RX.dot(RX).dot(RZ),
  RX.dot(RX).dot(RZ).dot(RZ),
  RX.dot(RX).dot(RZ).dot(RZ).dot(RZ),
  # Positive X pointing to the top possibilities.
  RY.dot(RY).dot(RY),
  RY.dot(RY).dot(RY).dot(RZ),
  RY.dot(RY).dot(RY).dot(RZ).dot(RZ),
  RY.dot(RY).dot(RY).dot(RZ).dot(RZ).dot(RZ),
  # Negative X pointing to the top possibilities.
  RY,
  RY.dot(RZ),
  RY.dot(RZ).dot(RZ),
  RY.dot(RZ).dot(RZ).dot(RZ),
  # Positive Y pointing to the top possibilities.
  RX,
  RX.dot(RZ),
  RX.dot(RZ).dot(RZ),
  RX.dot(RZ).dot(RZ).dot(RZ),
  # Negative Y pointing to the top possibilities.
  RX.dot(RX).dot(RX),
  RX.dot(RX).dot(RX).dot(RZ),
  RX.dot(RX).dot(RX).dot(RZ).dot(RZ),
  RX.dot(RX).dot(RX).dot(RZ).dot(RZ).dot(RZ),
]


def ReadScannerDetectedCoordinates(path):
  with open(path) as f:
    scanner_id = 0
    all_scanner_values = []
    scanner_values = []
    for line in f.readlines():
      line = line.strip()
      mobj = re.match('--- scanner ([0-9]*) ---', line)
      if mobj:
        assert(mobj.group(1) == str(scanner_id))
        continue
      if not line:
        scanner_id += 1
        all_scanner_values.append(np.array(scanner_values))
        scanner_values = []
        continue
      row = [int(str_value.strip()) for str_value in line.split(',')]
      scanner_values.append(row)
    all_scanner_values.append(np.array(scanner_values))
    return all_scanner_values


def DoCoordinatesCorrelate(left_coordinates, right_coordinates):
  left_set = set([tuple(row) for row in left_coordinates])
  right_set = set([tuple(row) for row in right_coordinates])
  intesection_len = len(left_set.intersection(right_set))
  if intesection_len >= 12:
    return True
  return False


def DetectSimilarScannerCoordinates(base_scanner_coordinates, other_scanner_coordinates):
  for i in range(len(base_scanner_coordinates)):
    for j in range(len(other_scanner_coordinates)):
      other_shift = base_scanner_coordinates[i] - other_scanner_coordinates[j]
      if DoCoordinatesCorrelate(base_scanner_coordinates, other_scanner_coordinates + other_shift):
        return other_shift
  return None


def FindRelationBetweenTwoScanners(base_scanner_coordinates, other_scanner_coordinates):
  '''Attempts to find the relationship between two scanners.

  If one is found, the location and orientation of the "other scanner" is returned relative to the base scanner.
  The location is returned as a row vector.
  The orientation is returned as an index into ALL_POSSIBLE_ROTATIONS.
  '''
  for rotation_index in range(len(ALL_POSSIBLE_ROTATIONS)):
    rotation_matrix = ALL_POSSIBLE_ROTATIONS[rotation_index]
    rotated_other_scanner_coordinates = other_scanner_coordinates.dot(rotation_matrix)
    other_scanner_shift = DetectSimilarScannerCoordinates(base_scanner_coordinates, rotated_other_scanner_coordinates)
    if other_scanner_shift is not None:
      return other_scanner_shift, rotation_index
  return None


def ConstructGlobalCoordinatesMap(scanners_coordinates):
  '''Take a list of arrays each containing coordinates pertaining to a scanner and construct a global map of these coordinates.

  Returns coordinates as tuples in reference to the first scanner (index 0).

  Returns None if the global map could not be constructed.
  '''
  assert(len(scanners_coordinates) > 0)
  scanner_pos_rot_directory = {0: (np.array([0, 0, 0]) ,0)}  # in reference to scanner 0.
  pairs_checked = defaultdict(lambda: False)
  while True:
    resolved_scanners = set(scanner_pos_rot_directory.keys())
    unresolved_scanners = set(range(len(scanners_coordinates))) - resolved_scanners
    scanners_resolved_this_round = 0
    if not unresolved_scanners:
      break
    for resolved_scanner in resolved_scanners:
      for unresolved_scanner in unresolved_scanners:
        # Avoid checking redundant pairs.
        if pairs_checked[(resolved_scanner, unresolved_scanner)]:
          continue
        pairs_checked[(resolved_scanner, unresolved_scanner)] = True
        # Scanner has already been resolved.
        if unresolved_scanner in scanner_pos_rot_directory.keys():
          continue

        # Translate the resolved scanner to scanner 0 or the global coordinates.
        rotated_and_shifted_resolved_scanner = scanners_coordinates[resolved_scanner].dot(ALL_POSSIBLE_ROTATIONS[scanner_pos_rot_directory[resolved_scanner][1]]) + scanner_pos_rot_directory[resolved_scanner][0]
        pos_rot = FindRelationBetweenTwoScanners(rotated_and_shifted_resolved_scanner, scanners_coordinates[unresolved_scanner])
        if pos_rot is not None:
          scanners_resolved_this_round += 1
          scanner_pos_rot_directory[unresolved_scanner] = (pos_rot[0], pos_rot[1])
          break
    if scanners_resolved_this_round == 0:
      print('Warning: No scanners resolved this round!!!')

  manhattan_distances = []
  for i in range(len(scanners_coordinates)):
    for j in range(i + 1, len(scanners_coordinates)):
      i_position = scanner_pos_rot_directory[i][0]
      j_position = scanner_pos_rot_directory[j][0]
      diff = i_position - j_position
      manhattan_distances.append(np.linalg.norm(diff, ord=1))

  all_coordinate_sets = []
  for scanner_id in range(len(scanners_coordinates)):
    scanner_translated_coordinates = scanners_coordinates[scanner_id].dot(ALL_POSSIBLE_ROTATIONS[scanner_pos_rot_directory[scanner_id][1]]) + scanner_pos_rot_directory[scanner_id][0]
    scanner_coordinates = set([tuple(row) for row in scanner_translated_coordinates])
    all_coordinate_sets.extend(scanner_coordinates)
  return set(all_coordinate_sets), max(manhattan_distances)


def Test():
  scanners_coordinates = ReadScannerDetectedCoordinates('example.txt')
  scanner_1_to_0_pos_rot = FindRelationBetweenTwoScanners(scanners_coordinates[0], scanners_coordinates[1])
  assert(np.array_equal(scanner_1_to_0_pos_rot[0], np.array([68,-1246,-43])))
  scanner_4_to_1_pos_rot = FindRelationBetweenTwoScanners(scanners_coordinates[1], scanners_coordinates[4])
  assert(np.array_equal(np.array([-20,-1133,1061]), scanner_4_to_1_pos_rot[0].dot(ALL_POSSIBLE_ROTATIONS[scanner_1_to_0_pos_rot[1]]) + scanner_1_to_0_pos_rot[0]))
  coordinates, _ = ConstructGlobalCoordinatesMap(scanners_coordinates)
  assert(len(coordinates) == 79)


def SolvePartsOneAndTwo():
  scanners_coordinates = ReadScannerDetectedCoordinates('input.txt')
  coordinates, largest_manhattan_distance = ConstructGlobalCoordinatesMap(scanners_coordinates)
  print(f'Part 1: Number of unique coordinates = {len(coordinates)}')
  print(f'Part 2: Largest manhattan distance = {largest_manhattan_distance}')
  assert(len(coordinates) == 428)
  assert(largest_manhattan_distance == 12140.0)


def Main():
  print('Hello Day 19!')
  Test()
  SolvePartsOneAndTwo()


if __name__ == '__main__':
  Main()