#!/usr/bin/env python3 


class BitReader(object):

  def __init__(self, hex_str):
    self.hex_str = hex_str
    self.hex_str_index = 0
    self.buffer_value = 0
    self.buffer_bit_count = 0

  def _FillBuffer(self):
    if self.hex_str_index > len(self.hex_str):
      raise Exception('Anyhow, you tried to read beyond the hexadecimal string.')
    self.buffer_value = self.buffer_value << 4 | int(self.hex_str[self.hex_str_index], 16)
    self.hex_str_index += 1
    self.buffer_bit_count += 4

  def ReadNBits(self, bit_count):
    while bit_count >= self.buffer_bit_count:
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
  if ptype == 4:  # Literal value packet.
    more_quartets = 1
    while more_quartets:
      more_quartets = bit_reader.ReadNBits(1)
      quartet = bit_reader.ReadNBits(4)
      packet_size_in_bits += 5
  else:
    length_type_id = bit_reader.ReadNBits(1)
    packet_size_in_bits += 1
    if length_type_id == 0:  # Next 15 bits represents size of subpackets in bits.
      declared_subpackets_size_in_bits = bit_reader.ReadNBits(15)
      packet_size_in_bits += 15
      parsed_subpackets_size_in_bits = 0
      while parsed_subpackets_size_in_bits < declared_subpackets_size_in_bits:
        size_in_bits, version = ParsePacket(bit_reader)
        parsed_subpackets_size_in_bits += size_in_bits
        version_sum += version
      assert(parsed_subpackets_size_in_bits == declared_subpackets_size_in_bits)
      packet_size_in_bits += parsed_subpackets_size_in_bits
    else:  # Next 11 bits represents number of subpackets.
      declared_subpackets_count = bit_reader.ReadNBits(11)
      packet_size_in_bits += 11
      for _ in range(declared_subpackets_count):
        size_in_bits, version = ParsePacket(bit_reader)
        packet_size_in_bits += size_in_bits
        version_sum += version
  return packet_size_in_bits, version_sum
 

def Test():
  _, version_sum = ParsePacket(BitReader('8A004A801A8002F478'))
  assert(version_sum == 16)
  _, version_sum = ParsePacket(BitReader('620080001611562C8802118E34'))
  assert(version_sum == 12)
  _, version_sum = ParsePacket(BitReader('C0015000016115A2E0802F182340'))
  assert(version_sum == 23)
  _, version_sum = ParsePacket(BitReader('A0016C880162017C3686B18A3D4780'))
  assert(version_sum == 31)


def SolvePartOne():
  hex_str = ReadHexadecimalString('input.txt')
  _, version_sum = ParsePacket(BitReader(hex_str))
  print(f'Part 1: Version sum = {version_sum}')


def SolvePartTwo():
  pass


def Main():
  print('Hello Day 16!')
  Test()
  SolvePartOne()
  SolvePartTwo()


if __name__ == '__main__':
  Main()