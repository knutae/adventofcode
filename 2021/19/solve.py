
def parse_scanner(scanner):
    lines = scanner.split('\n')
    assert lines[0].startswith('--- scanner ')
    return [tuple((int(x) for x in line.split(','))) for line in lines[1:]]

def parse_file(filename):
    with open(filename) as f:
        data = f.read()
    scanners = data.strip().split('\n\n')
    return [parse_scanner(scanner) for scanner in scanners]


def rot2(y,z):
    yield y,z
    yield -z,y
    yield -y,-z
    yield z,-y

assert len(set(rot2(1,2))) == 4

def rot3(x,y,z):
    # X positive: x,y,z
    for a,b in rot2(y,z):
        yield x,a,b
    # X negative: -x,-y,z
    for a,b in rot2(-y,z):
        yield -x,a,b
    # Y positive: y,-x,z
    for a,b in rot2(-x,z):
        yield y,a,b
    # Y negative: -y,x,z
    for a,b in rot2(x,z):
        yield -y,a,b
    # Z positive: z,y,-x
    for a,b in rot2(y,-x):
        yield z,a,b
    # Z negative: -z,y,x
    for a,b in rot2(y,x):
        yield -z,a,b

# just checks that rotations are uniqe, not that they are correct...
assert len(set(rot3(1,2,3))) == 24

def scanner_rotations(points):
    scanners = [[None]*len(points) for _ in range(24)]
    for pi, point in enumerate(points):
        for ri, p in enumerate(rot3(*point)):
            scanners[ri][pi] = p
    return scanners

def test_rotations():
    example = [(-1,-1,1), (-2,-2,2), (-3,-3,3), (-2,-3,1), (5,6,-4), (8,0,7)]
    rotations = scanner_rotations(example)
    assert len(rotations) == 24
    assert rotations[0] == example
    assert [(1,-1,1), (2,-2,2), (3,-3,3), (2,-1,3), (-5,4,-6), (-8,-7,0)] in rotations
    assert [(1,-1,1), (2,-2,2), (3,-3,3), (2,-1,3), (-5,4,-6), (-8,-7,0)] in rotations
    assert [(1,1,-1), (2,2,-2), (3,3,-3), (1,3,-2), (-4,-6,5), (7,0,8)] in rotations
    assert [(1,1,1), (2,2,2), (3,3,3), (3,1,2), (-6,-4,-5), (0,7,-8)] in rotations

test_rotations()

def vec_add(a, b):
    x0,y0,z0 = a
    x1,y1,z1 = b
    return x0+x1,y0+y1,z0+z1

def vec_sub(a, b):
    x0,y0,z0 = a
    x1,y1,z1 = b
    return x0-x1,y0-y1,z0-z1

def translate(scanner, amount):
    return [vec_add(p, amount) for p in scanner]

def try_reorient(scanner1, scanner2):
    set1 = set(scanner1)
    for rotation in scanner_rotations(scanner2):
        # can skip 11 points for each scanner since at least 12 points must overlap
        for p2 in rotation[11:]:
            for p1 in scanner1[11:]:
                amount = vec_sub(p1, p2)
                translated = translate(rotation, amount)
                assert p1 in translated
                overlap_count = len(set(translated) & set1)
                assert overlap_count > 0
                #print(f'Move {amount}: {overlap_count} overlap')
                if overlap_count >= 12:
                    return amount, translated
    return None, None

def test_reorient():
    scanners = parse_file('example')
    _, reorient1 = try_reorient(scanners[0], scanners[1])
    assert reorient1 is not None
    overlap = set(reorient1) & set(scanners[0])
    assert len(overlap) == 12
    assert overlap == {
        (-618,-824,-621),
        (-537,-823,-458),
        (-447,-329,318),
        (404,-588,-901),
        (544,-627,-890),
        (528,-643,409),
        (-661,-816,-575),
        (390,-675,-793),
        (423,-701,434),
        (-345,-311,381),
        (459,-707,401),
        (-485,-357,347),
    }

test_reorient()

def reorient_all(scanners):
    reoriented = [scanners[0]]
    remaining = scanners[1:]
    translate_amounts = [(0,0,0)]
    while len(remaining) > 0:
        found_index = None
        for i, candidate in enumerate(remaining):
            for r in reoriented:
                amount, reoriented_candidate = try_reorient(r, candidate)
                if reoriented_candidate is not None:
                    reoriented.append(reoriented_candidate)
                    translate_amounts.append(amount)
                    found_index = i
                    break
            if found_index is not None:
                break
        assert found_index is not None
        del remaining[found_index]
    return translate_amounts, reoriented

def solve1(scanners):
    _, reoriented = reorient_all(scanners)
    all_beacons = set()
    for r in reoriented:
        all_beacons |= set(r)
    #print(all_beacons)
    return len(all_beacons)

def manhattan_distance(a, b):
    x0,y0,z0 = a
    x1,y1,z1 = b
    return abs(x0-x1)+abs(y0-y1)+abs(z0-z1)

def solve2(scanners):
    translate_amounts, _ = reorient_all(scanners)
    return max(manhattan_distance(a, b) for a in translate_amounts for b in translate_amounts if a != b)

assert solve1(parse_file('example')) == 79
assert solve2(parse_file('example')) == 3621
print(solve1(parse_file('input')))
print(solve2(parse_file('input')))
