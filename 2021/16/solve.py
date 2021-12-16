import math

def parse_to_bin(hex_input):
    hex_input = hex_input.strip()
    return bin(int(hex_input, 16))[2:].zfill(len(hex_input)*4)

class BinStream:
    def __init__(self, bin_input):
        self.bin_input = bin_input
        self.offset = 0

    def read_int(self, bits):
        assert self.offset + bits <= len(self.bin_input), f'Cannot read {bits} bits at offset={self.offset} len={len(self.bin_input)}'
        n = int(self.bin_input[self.offset:self.offset+bits], 2)
        self.offset += bits
        return n

    def generate_packets(self):
        while self.has_more():
            yield self.parse_packet()

    def parse_packet(self):
        version = self.read_int(3)
        type_id = self.read_int(3)
        if type_id == 4:
            # parse literal value
            literal = 0
            last_block = False
            while not last_block:
                last_block = self.read_int(1) == 0
                literal = (literal << 4) + self.read_int(4)
            return version, type_id, literal, []
        else:
            # parse operator with sub-packets
            length_type_id = self.read_int(1)
            if length_type_id == 0:
                total_bit_length = self.read_int(15)
                assert total_bit_length >= 0 and total_bit_length <= self.offset + len(self.bin_input)
                sub_stream = BinStream(self.bin_input[self.offset:self.offset+total_bit_length])
                sub_packets = list(sub_stream.generate_packets())
                self.offset += total_bit_length
            else:
                sub_packet_count = self.read_int(11)
                sub_packets = []
                for _ in range(sub_packet_count):
                    sub_packets.append(self.parse_packet())
            return version, type_id, None, sub_packets

    def has_more(self):
        return self.offset + 8 < len(self.bin_input)

def parse_packets(hex_input):
    s = BinStream(parse_to_bin(hex_input))
    return list(s.generate_packets())

assert parse_packets('D2FE28') == [(6, 4, 2021, [])]
assert parse_packets('38006F45291200') == [(1, 6, None, [(6, 4, 10, []), (2, 4, 20, [])])]
assert parse_packets('EE00D40C823060') == [(7, 3, None, [(2, 4, 1, []), (4, 4, 2, []), (1, 4, 3, [])])]

def version_sum(packets):
    return sum(
        version + version_sum(sub_packets)
        for version, _, _, sub_packets in packets
    )

def solve1(hex_input):
    return version_sum(parse_packets(hex_input))

assert solve1('8A004A801A8002F478') == 16
assert solve1('620080001611562C8802118E34') == 12
assert solve1('C0015000016115A2E0802F182340') == 23
assert solve1('A0016C880162017C3686B18A3D4780') == 31

def evaluate(packet):
    _, type_id, literal, sub_packets = packet
    if type_id == 0:
        return sum(evaluate(p) for p in sub_packets)
    if type_id == 1:
        return math.prod(evaluate(p) for p in sub_packets)
    if type_id == 2:
        return min(evaluate(p) for p in sub_packets)
    if type_id == 3:
        return max(evaluate(p) for p in sub_packets)
    if type_id == 4:
        assert literal is not None
        return literal
    if type_id == 5:
        a, b = sub_packets
        return int(evaluate(a) > evaluate(b))
    if type_id == 6:
        a, b = sub_packets
        return int(evaluate(a) < evaluate(b))
    if type_id == 7:
        a, b = sub_packets
        return int(evaluate(a) == evaluate(b))
    assert False

def solve2(hex_input):
    packets = parse_packets(hex_input)
    assert len(packets) == 1
    return evaluate(packets[0])

assert solve2('C200B40A82') == 3
assert solve2('04005AC33890') == 54
assert solve2('880086C3E88112') == 7
assert solve2('CE00C43D881120') == 9
assert solve2('D8005AC2A8F0') == 1
assert solve2('F600BC2D8F') == 0
assert solve2('9C005AC2F8F0') == 0
assert solve2('9C0141080250320F1802104A08') == 1

with open('input') as f:
    hex_input = f.read()

print(solve1(hex_input))
print(solve2(hex_input))
