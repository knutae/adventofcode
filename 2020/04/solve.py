TEST_INPUT = '''
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
'''

def parse_group(input):
    pairs = dict()
    for kv in input.split():
        assert ':' in kv
        [k, v] = kv.split(':')
        pairs[k] = v
    return pairs

def parse(input):
    return [parse_group(x) for x in input.strip().split('\n\n')]

def solve1(passports):
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} # not cid
    valid = 0
    for passport in passports:
        if all(k in passport for k in required):
            valid += 1
    return valid

def valid_range(n, at_least, at_most):
    return int(n) in range(at_least, at_most + 1)

def valid_hgt(hgt):
    if hgt.endswith('cm'):
        return valid_range(hgt[:-2], 150, 193)
    elif hgt.endswith('in'):
        return valid_range(hgt[:-2], 59, 76)
    else:
        return False

def valid_hcl(hcl):
    if len(hcl) != 7 or hcl[0] != '#':
        return False
    try:
        return int(hcl[1:], 16) >= 0
    except ValueError:
        return False

def valid_ecl(ecl):
    return ecl in {'amb','blu','brn','gry','grn','hzl','oth'}

def valid_pid(pid):
    return len(pid) == 9 and pid.isdigit()

def valid(passport):
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} # not cid
    return (
        all(k in passport for k in required) and
        valid_range(passport['byr'], 1920, 2002) and
        valid_range(passport['iyr'], 2010, 2020) and
        valid_range(passport['eyr'], 2020, 2030) and
        valid_hgt(passport['hgt']) and
        valid_hcl(passport['hcl']) and
        valid_ecl(passport['ecl']) and
        valid_pid(passport['pid'])
    )

INVALID = '''
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
'''

VALID = '''
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
'''

def solve2(passports):
    return len([p for p in passports if valid(p)])

passports = parse(TEST_INPUT)
assert solve1(passports) == 2
assert solve2(parse(INVALID)) == 0
assert solve2(parse(VALID)) == 4
with open('input') as f:
    passports = parse(f.read())
#print(solve1(passports))
print(solve2(passports))
