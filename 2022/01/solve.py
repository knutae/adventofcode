def solve1(input):
    sections = input.split('\n\n')
    sections = [[int(line) for line in section.split('\n') if line] for section in sections]
    #print(sections)
    return max(sum(section) for section in sections)

def solve2(input):
    sections = input.split('\n\n')
    sections = [[int(line) for line in section.split('\n') if line] for section in sections]
    #print(sections)
    sums = list(map(sum, sections))
    sums.sort(reverse=True)
    #print(sums)
    return sum(sums[0:3])

with open('input') as f:
    input = f.read()
    print(solve1(input))
    print(solve2(input))
