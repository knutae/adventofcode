import sys

data = sys.stdin.read().strip()
layers = [data[i:i+25*6] for i in range(0, len(data), 25*6)]
#fewest_zeroes = min((layer for layer in layers), key=lambda x:x.count('0'))
#print(fewest_zeroes.count('1')*fewest_zeroes.count('2'))

image_data = ['2' for _ in range(25*6)]

for layer in layers:
    for i in range(len(image_data)):
        if image_data[i] == '2':
            image_data[i] = layer[i]

image_data = ''.join(image_data).replace('0', ' ').replace('1', 'X')
for i in range(0, 25*6, 25):
    print(image_data[i:i+25])
