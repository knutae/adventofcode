def parse(input):
    return [int(c) for c in input]

def previous_cup(cup, max):
    return max if cup == 1 else cup - 1

class Cups:
    def __init__(self, cups):
        # cup node: [prev_index, next_index]. the list index is the label
        self.nodes = [[None, None] for i in range(len(cups) + 1)]
        # circular list: initialize a sentinel node
        self.current_cup = cups[0]
        self.nodes[self.current_cup] = [self.current_cup, self.current_cup]
        # ... then insert the rest
        prev_cup = self.current_cup
        for cup in cups[1:]:
            self.insert_after(prev_cup, cup)
            prev_cup = cup

    def insert_after(self, before, cup):
        assert cup >= 1 and cup < len(self.nodes)
        cup_node = self.nodes[cup]
        assert cup_node == [None, None], f"Cup {cup} already present"
        before_node = self.nodes[before]
        after = before_node[1]
        after_node = self.nodes[after]
        cup_node[0] = before
        cup_node[1] = after
        before_node[1] = cup
        after_node[0] = cup

    def _last_cup(self):
        self.nodes[self.current_cup][0]

    def append(self, cup):
        last = self.nodes[self.current_cup][0]
        self.insert_after(last, cup)

    def after(self, cup):
        r = self.nodes[cup][1]
        assert r is not None
        return r

    def remove(self, cup):
        assert cup != self.current_cup
        node = self.nodes[cup]
        assert None not in node
        [before, after] = node
        self.nodes[before][1] = after
        self.nodes[after][0] = before
        node[0] = None
        node[1] = None

    def __iter__(self):
        first = self.current_cup
        current = first
        while True:
            yield current
            current = self.nodes[current][1]
            if current == first:
                return

    def __str__(self):
        tmp = ','.join(str(cup) for cup in self)
        return f'Cups([{tmp}])'

    def step(self):
        a = self.after(self.current_cup)
        b = self.after(a)
        c = self.after(b)
        self.remove(a)
        self.remove(b)
        self.remove(c)
        max = len(self.nodes) - 1
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
