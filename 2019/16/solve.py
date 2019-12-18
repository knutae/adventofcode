import abc
import operator
import sys

def enumerate_ranges(index, length):
    mul = index + 1
    inc = mul * 2
    start = mul-1
    while True:
        yield start, min(length, start + mul), 1
        start += inc
        if start >= length:
            return
        yield start, min(length, start + mul), -1
        start += inc
        if start >= length:
            return

def calculate_cumsum(signal):
    result = [0] * (len(signal) + 1)
    for i, n in enumerate(signal):
        result[i+1] = result[i] + n
    return result

def phase(signal):
    return fast_phase(signal, calculate_ranges(len(signal)))

def fast_phase(signal, ranges):
    result = []
    cumsum = calculate_cumsum(signal)
    for index in range(len(signal)):
        s = 0
        for start, stop, p in ranges[index]:
            s += (cumsum[stop]-cumsum[start])*p
        result.append(abs(s) % 10)
    #print(result)
    return result

def calculate_ranges(length):
    return [list(enumerate_ranges(i, length)) for i in range(length)]

def phases(signal, n):
    ranges = calculate_ranges(len(signal))
    for _ in range(n):
        #print(f"phase {i}")
        signal = fast_phase(signal, ranges)
    return signal

def solve(input, n=100):
    signal = [int(x) for x in input]
    signal = phases(signal, n)
    signal = signal[0:8]
    return ''.join(str(x) for x in signal)

def solve2(input):
    offset = int(input[0:7])
    #print(f'offset {offset}')
    signal = [int(x) for x in input] * 10000
    signal = phases(signal, 100)
    signal = signal[offset:offset+8]
    return ''.join(str(x) for x in signal)

def test():
    assert phase([1,2,3,4,5,6,7,8]) == [4,8,2,2,6,1,5,8]
    assert phase([4,8,2,2,6,1,5,8]) == [3,4,0,4,0,4,3,8]
    assert solve('12345678', 1) == '48226158'
    assert solve('80871224585914546619083218645595') == '24176176'
    assert solve('19617804207202209144916044189917') == '73745418'
    assert solve('69317163492948606335995924319873') == '52432133'
    assert solve2('03036732577212944063491565474664') == '84462026'
    assert solve2('02935109699940807407585447034323') == '78725270'
    assert solve2('03081770884921959731165446850517') == '53553731'

#import cProfile
#cProfile.run('test()')
#test()

INPUT = '59740570066545297251154825435366340213217767560317431249230856126186684853914890740372813900333546650470120212696679073532070321905251098818938842748495771795700430939051767095353191994848143745556802800558539768000823464027739836197374419471170658410058272015907933865039230664448382679990256536462904281204159189130560932257840180904440715926277456416159792346144565015659158009309198333360851441615766440174908079262585930515201551023564548297813812053697661866316093326224437533276374827798775284521047531812721015476676752881281681617831848489744836944748112121951295833143568224473778646284752636203058705797036682752546769318376384677548240590'

#print(solve(INPUT))
print(solve2(INPUT))
