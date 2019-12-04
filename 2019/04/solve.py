
def is_password_candidate(n):
    last_d = -1
    found_double = False
    for c in str(n):
        d = int(c)
        if d < last_d:
            return False
        if d == last_d:
            found_double = True
        last_d = d
    return found_double

assert(is_password_candidate(111111) == True)
assert(is_password_candidate(223450) == False)
assert(is_password_candidate(123789) == False)

def is_password_candidate_2(n):
    doubles = set()
    triples = set()
    n = [int(c) for c in str(n)]
    for i, c in enumerate(n):
        d = int(c)
        d_1 = n[i-1] if i > 0 else -1
        if d < d_1:
            return False
        d_2 = n[i-2] if i > 1 else -1
        if d == d_1:
            doubles.add(d)
            if d == d_2:
                triples.add(d)
    return len(doubles - triples) > 0

assert(is_password_candidate_2(111111) == False)
assert(is_password_candidate_2(223450) == False)
assert(is_password_candidate_2(123789) == False)
assert(is_password_candidate_2(112233) == True)
assert(is_password_candidate_2(123444) == False)
assert(is_password_candidate_2(111122) == True)

def solve1():
    print(sum(is_password_candidate(n) for n in range(278384,824795+1)))

def solve2():
    print(sum(is_password_candidate_2(n) for n in range(278384,824795+1)))

solve1()
solve2()
