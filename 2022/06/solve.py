def marker_index(input, marker_length):
    for i in range(marker_length, len(input)):
        if len(set(input[i-marker_length:i])) == marker_length:
            return i

def solve1(input):
    return marker_index(input, 4)

def solve2(input):
    return marker_index(input, 14)

assert solve1('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
assert solve1('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert solve1('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert solve1('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert solve1('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

assert solve2('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 19
assert solve2('bvwbjplbgvbhsrlpgdmjqwftvncz') == 23
assert solve2('nppdvjthqldpwncqszvftbrmjlhg') == 23
assert solve2('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 29
assert solve2('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 26

with open('input') as f:
    input = f.read().strip()

print(solve1(input))
print(solve2(input))