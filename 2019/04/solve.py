
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

def solve1():
    print(sum(is_password_candidate(n) for n in range(278384,824795+1)))

solve1()