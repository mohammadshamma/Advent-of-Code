#!/usr/bin/env python3 

import math


class BitReader(object):

  def __init__(self, hex_str):
    self.hex_str = hex_str
    self.hex_str_index = 0
    self.buffer_value = 0
    self.buffer_bit_count = 0

  def _FillBuffer(self):
    if self.hex_str_index >= len(self.hex_str):
      raise Exception('Anyhow, you tried to read beyond the hexadecimal string.')
    self.buffer_value = self.buffer_value << 4 | int(self.hex_str[self.hex_str_index], 16)
    self.hex_str_index += 1
    self.buffer_bit_count += 4

  def ReadNBits(self, bit_count):
    while bit_count > self.buffer_bit_count:
      self._FillBuffer()
    value = self.buffer_value >> (self.buffer_bit_count - bit_count)
    self.buffer_value &= (2 ** (self.buffer_bit_count - bit_count)) - 1
    self.buffer_bit_count = self.buffer_bit_count - bit_count
    return value


def ReadHexadecimalString(path):
  with open(path) as f:
    return f.readline().strip()
 

def ParsePacket(bit_reader):
  version = bit_reader.ReadNBits(3)
  version_sum = version
  ptype = bit_reader.ReadNBits(3)
  packet_size_in_bits = 6
  value = None
  if ptype == 4:  # Literal value packet.
    more_quartets = 1
    value = 0
    while more_quartets:
      more_quartets = bit_reader.ReadNBits(1)
      quartet = bit_reader.ReadNBits(4)
      value = value << 4 | quartet
      packet_size_in_bits += 5
  else:
    length_type_id = bit_reader.ReadNBits(1)
    packet_size_in_bits += 1
    subpacket_values = []
    if length_type_id == 0:  # Next 15 bits represents size of subpackets in bits.
      declared_subpackets_size_in_bits = bit_reader.ReadNBits(15)
      packet_size_in_bits += 15
      parsed_subpackets_size_in_bits = 0
      while parsed_subpackets_size_in_bits < declared_subpackets_size_in_bits:
        size_in_bits, version, value = ParsePacket(bit_reader)
        parsed_subpackets_size_in_bits += size_in_bits
        version_sum += version
        subpacket_values.append(value)
      assert(parsed_subpackets_size_in_bits == declared_subpackets_size_in_bits)
      packet_size_in_bits += parsed_subpackets_size_in_bits
    else:  # Next 11 bits represents number of subpackets.
      declared_subpackets_count = bit_reader.ReadNBits(11)
      packet_size_in_bits += 11
      for _ in range(declared_subpackets_count):
        size_in_bits, version, value = ParsePacket(bit_reader)
        packet_size_in_bits += size_in_bits
        version_sum += version
        subpacket_values.append(value)
    if ptype == 0:  # sum
      value = sum(subpacket_values)
    elif ptype == 1:  # product
      value = math.prod(subpacket_values)
    elif ptype == 2:  # minimum
      value = min(subpacket_values)
    elif ptype == 3:  # minimum
      value = max(subpacket_values)
    elif ptype == 5:  # greater than
      assert(len(subpacket_values) == 2)
      value = 0
      if subpacket_values[0] > subpacket_values[1]:
        value = 1
    elif ptype == 6:  # less than
      assert(len(subpacket_values) == 2)
      value = 0
      if subpacket_values[0] < subpacket_values[1]:
        value = 1
    elif ptype == 7:  # equal
      assert(len(subpacket_values) == 2)
      value = 0
      if subpacket_values[0] == subpacket_values[1]:
        value = 1

  return packet_size_in_bits, version_sum, value
 

def Test():

  # Part 1
  def GetVersionSumOf(hex_str):
    _, version_sum, _ = ParsePacket(BitReader(hex_str))
    return version_sum
  assert(GetVersionSumOf('8A004A801A8002F478') == 16)
  assert(GetVersionSumOf('620080001611562C8802118E34') == 12)
  assert(GetVersionSumOf('C0015000016115A2E0802F182340') == 23)
  assert(GetVersionSumOf('A0016C880162017C3686B18A3D4780') == 31)
  
  # Part 2
  def GetValueOf(hex_str):
    _, _, value = ParsePacket(BitReader(hex_str))
    return value
  assert(GetValueOf('C200B40A82') == 3)
  assert(GetValueOf('04005AC33890') == 54)
  assert(GetValueOf('880086C3E88112') == 7)
  assert(GetValueOf('CE00C43D881120') == 9)
  assert(GetValueOf('D8005AC2A8F0') == 1)
  assert(GetValueOf('F600BC2D8F') == 0)
  assert(GetValueOf('9C005AC2F8F0') == 0)
  assert(GetValueOf('9C0141080250320F1802104A08') == 1)


def SolvePartOne():
  hex_str = ReadHexadecimalString('input.txt')
  _, version_sum, _ = ParsePacket(BitReader(hex_str))
  print(f'Part 1: Version sum = {version_sum}')
  assert(version_sum == 860)


def SolvePartTwo():
  hex_str = ReadHexadecimalString('input.txt')
  _, _, value = ParsePacket(BitReader(hex_str))
  print(f'Part 2: Packet value = {value}')
  assert(value == 470949537659)


def Main():
  print('Hello Day 16!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()