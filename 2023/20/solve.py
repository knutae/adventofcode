import abc
import collections

EXAMPLE1 = '''
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''

EXAMPLE2 = '''
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''

class Module(abc.ABC):
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
        self.inputs = None

    @abc.abstractmethod
    def receive_pulse(self, input_module, high):
        return None

    def register_inputs(self, inputs):
        assert self.inputs is None
        self.inputs = inputs

    def process_pulse(self, input_module, high):
        res = self.receive_pulse(input_module, high)
        if res is None:
            return
        for output in self.outputs:
            yield output, res

    def __repr__(self):
        return f'{type(self).__name__}(name={self.name}, inputs={self.inputs}, outputs={self.outputs})'

class FlipFlop(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.off = True

    def receive_pulse(self, _, high):
        if high:
            return None
        if self.off:
            self.off = False
            return True
        else:
            self.off = True
            return False

class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.input_signals = None

    def register_inputs(self, inputs):
        super().register_inputs(inputs)
        self.input_signals = {x: False for x in inputs}

    def receive_pulse(self, input_module, high):
        assert input_module in self.input_signals
        self.input_signals[input_module] = high
        if all(self.input_signals.values()):
            return False
        else:
            return True

class Broadcaster(Module):
    def receive_pulse(self, _, high):
        return high

def parse_module(line):
    lhs, rhs = line.split(' -> ')
    outputs = rhs.split(', ')
    if lhs[0] == '%':
        return FlipFlop(lhs[1:], outputs)
    elif lhs[0] == '&':
        return Conjunction(lhs[1:], outputs)
    else:
        return Broadcaster(lhs, outputs)

def parse(data):
    modules = [parse_module(line) for line in data.strip().split('\n')]
    input_map = collections.defaultdict(list)
    for m in modules:
        for output in m.outputs:
            input_map[output].append(m.name)
    for m in modules:
        m.register_inputs(input_map[m.name])
    return {m.name: m for m in modules}

def step(modules):
    low_count = 0
    high_count = 0
    signals = collections.deque([('button', 'broadcaster', False)])
    while signals:
        input_name, name, high = signals.popleft()
        if high:
            high_count += 1
        else:
            low_count += 1
        if name in modules:
            for output_name, output_high in modules[name].process_pulse(input_name, high):
                #print(input_name, name, high, "-->", output_name, output_high)
                signals.append((name, output_name, output_high))
    return low_count, high_count

def solve1(data):
    modules = parse(data)
    total_low_count = 0
    total_high_count = 0
    for _ in range(1000):
        low_count, high_count = step(modules)
        total_low_count += low_count
        total_high_count += high_count
    return total_low_count * total_high_count

assert solve1(EXAMPLE1) == 32000000
assert solve1(EXAMPLE2) == 11687500

with open('input') as f:
    data = f.read()

print(solve1(data))
