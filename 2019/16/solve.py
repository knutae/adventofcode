import operator
import sys

BASE_PATTERN = [0, 1, 0, -1]

def pattern(index, length):
    result = []
    mul = index + 1
    while len(result) <= length:
        for b in [0, 1, 0, -1]:
            for _ in range(mul):
                result.append(b)
    return result[1:length+1]

def phase(signal):
    result = []
    for index in range(len(signal)):
        s = sum(p*n for p, n in zip(signal, pattern(index, len(signal))))
        result.append(abs(s) % 10)
    return result

def phases(signal, n):
    for _ in range(n):
        signal = phase(signal)
    return signal

def solve(input, n=100):
    signal = [int(x) for x in input]
    signal = phases(signal, n)
    signal = signal[0:8]
    return ''.join(str(x) for x in signal)

def test():
    assert pattern(0, 8) == [1, 0, -1, 0, 1, 0, -1, 0]
    assert pattern(1, 8) == [0, 1, 1, 0, 0, -1, -1, 0]
    assert pattern(2, 8) == [0, 0, 1, 1, 1, 0, 0, 0]
    assert phase([1,2,3,4,5,6,7,8]) == [4,8,2,2,6,1,5,8]
    assert phase([4,8,2,2,6,1,5,8]) == [3,4,0,4,0,4,3,8]
    assert solve('80871224585914546619083218645595') == '24176176'
    assert solve('19617804207202209144916044189917') == '73745418'
    assert solve('69317163492948606335995924319873') == '52432133'

test()

INPUT = '59740570066545297251154825435366340213217767560317431249230856126186684853914890740372813900333546650470120212696679073532070321905251098818938842748495771795700430939051767095353191994848143745556802800558539768000823464027739836197374419471170658410058272015907933865039230664448382679990256536462904281204159189130560932257840180904440715926277456416159792346144565015659158009309198333360851441615766440174908079262585930515201551023564548297813812053697661866316093326224437533276374827798775284521047531812721015476676752881281681617831848489744836944748112121951295833143568224473778646284752636203058705797036682752546769318376384677548240590'

print(solve(INPUT))
