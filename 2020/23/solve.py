def parse(input):
    return [int(c) for c in input]

def previous_cup(cup, max):
    return max if cup == 1 else cup - 1

class Cups:
    def __init__(self, cups):
        # for each cup label (index), maintain the label of the next cup
        self.next_cups = [None for i in range(len(cups) + 1)]
        # circular singly linked list: initialize a sentinel node
        self.current_cup = cups[0]
        self.next_cups[self.current_cup] = self.current_cup
        # ... then insert the rest
        prev_cup = self.current_cup
        for cup in cups[1:]:
            self.insert_after(prev_cup, cup)
            prev_cup = cup

    def insert_after(self, before, cup):
        assert cup >= 1 and cup < len(self.next_cups)
        assert self.next_cups[cup] is None, f"Cup {cup} already present"
        after = self.next_cups[before]
        self.next_cups[before] = cup
        self.next_cups[cup] = after

    def after(self, cup):
        r = self.next_cups[cup]
        assert r is not None
        return r

    def remove_after(self, cup):
        after = self.next_cups[cup]
        assert after != self.current_cup
        self.next_cups[cup] = self.next_cups[after]
        self.next_cups[after] = None
        return after

    def __iter__(self):
        first = self.current_cup
        current = first
        while True:
            yield current
            current = self.next_cups[current]
            if current == first:
                return

    def __str__(self):
        tmp = ','.join(str(cup) for cup in self)
        return f'Cups([{tmp}])'

    def step(self):
        a = self.remove_after(self.current_cup)
        b = self.remove_after(self.current_cup)
        c = self.remove_after(self.current_cup)
        max = len(self.next_cups) - 1
        dest_cup = previous_cup(self.current_cup, max)
        while dest_cup in (a,b,c):
            dest_cup = previous_cup(dest_cup, max)
        self.insert_after(dest_cup, a)
        self.insert_after(a, b)
        self.insert_after(b, c)
        self.current_cup = self.after(self.current_cup)

    def steps(self, n):
        for i in range(n):
            #if i > 0 and i % 100000 == 0:
            #    print(i)
            self.step()

def test_cups():
    cups = Cups([3,8,9,1,2,5,4,6,7])
    assert list(cups) == [3,8,9,1,2,5,4,6,7]
    cups.step()
    assert list(cups) == [2,8,9,1,5,4,6,7,3]
    cups.steps(9)
    assert list(cups) == [8,3,7,4,1,9,2,6,5]

test_cups()

def solve1(input, steps=100):
    cups = Cups(parse(input))
    cups.steps(steps)
    cups.current_cup = 1
    return ''.join(str(cup) for cup in cups)[1:]

assert solve1('389125467', 10) == '92658374'
assert solve1('389125467', 100) == '67384529'

def solve2(input):
    cups = parse(input)
    cups += range(len(cups) + 1, 1_000_001)
    assert len(cups) == 1_000_000
    cups = Cups(cups)
    cups.steps(10_000_000)
    a = cups.after(1)
    b = cups.after(a)
    #print(a, b, a*b)
    return a * b

assert solve2('389125467') == 149245887792

print(solve1('496138527'))
print(solve2('496138527'))
