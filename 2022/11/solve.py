from collections import deque
from dataclasses import dataclass
from typing import Callable

EXAMPLE = '''
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''

def operation_add(n: int) -> Callable[[int], int]:
    return lambda old: old + n

def operation_mult(n: int)-> Callable[[int], int]:
    return lambda old: old * n

def operation_square() -> Callable[[int], int]:
    return lambda old: old * old

@dataclass
class Monkey:
    index: int
    starting_items: list[int]
    operation: Callable[[int], int]
    divisible_by: int
    then_to: int
    else_to: int

def parse_int_after(line, separator):
    [_, r] = line.split(separator)
    return int(r)

def parse_monkey(input):
    [index, starting_items, operation, divisible_by, then_to, else_to] = input.split('\n')
    index = parse_int_after(index.rstrip(':'), ' ')
    [_, starting_items] = starting_items.split(': ')
    starting_items = [int(x) for x in starting_items.split(', ')]
    [_, operation] = operation.split(' = ')
    if operation == 'old * old':
        operation = operation_square()
    elif operation.startswith('old * '):
        operation = operation_mult(int(operation.split(' * ')[-1]))
    elif operation.startswith('old + '):
        operation = operation_add(int(operation.split(' + ')[-1]))
    else:
        assert False, f"Failed to parse operation {operation}"
    divisible_by = parse_int_after(divisible_by, ' by ')
    then_to = parse_int_after(then_to, ' monkey ')
    else_to = parse_int_after(else_to, ' monkey ')
    return Monkey(index, starting_items, operation, divisible_by, then_to, else_to)

def parse(input):
    return [parse_monkey(x) for x in input.strip().split('\n\n')]

def run_round(monkeys, items, inspected_counts):
    for i, monkey in enumerate(monkeys):
        while len(items[i]) > 0:
            inspected_counts[i] += 1
            item = items[i].popleft()
            item = monkey.operation(item)
            item //= 3
            if item % monkey.divisible_by == 0:
                target = monkey.then_to
            else:
                target = monkey.else_to
            items[target].append(item)

def print_items(round, items):
    print(f'Round {round}')
    for i, monkey_items in enumerate(items):
        print(f'Monkey {i}: {list(monkey_items)}')

def solve1(input):
    monkeys = parse(input)
    items = [deque(m.starting_items) for m in monkeys]
    inspected_counts = [0 for _ in monkeys]
    for _ in range(20):
        run_round(monkeys, items, inspected_counts)
        #print_items(round, items)
    sorted_counts = list(sorted(inspected_counts, reverse=True))
    return sorted_counts[0] * sorted_counts[1]

assert solve1(EXAMPLE) == 10605

with open('input') as f:
    input = f.read()

print(solve1(input))
