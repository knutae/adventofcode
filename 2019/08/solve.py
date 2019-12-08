import sys

data = sys.stdin.read().strip()
layers = [data[i:i+25*6] for i in range(0, len(data), 25*6)]
fewest_zeroes = min((layer for layer in layers), key=lambda x:x.count('0'))
print(fewest_zeroes.count('1')*fewest_zeroes.count('2'))
