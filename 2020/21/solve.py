EXAMPLE = '''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''

def parse_line(line):
    assert line.endswith(')')
    [ingredients, allergens] = line[:-1].split(' (contains ')
    ingredients = ingredients.split(' ')
    allergens = allergens.split(', ')
    return ingredients, allergens

def parse(input):
    return [parse_line(x) for x in input.strip().split('\n')]

def ingredients_possibly_containing_allergen(foods, allergen):
    return set.intersection(*(
        set(ingredients) for ingredients, allergens in foods if allergen in allergens
    ))

def solve1(input):
    foods = parse(input)
    all_allergens = set.union(*(set(allergens) for _, allergens in foods))
    all_ingredients = set.union(*(set(ingredients) for ingredients, _ in foods))
    ingredients_containing_allergens = set.union(*(
        ingredients_possibly_containing_allergen(foods, allergen)
        for allergen in all_allergens
    ))
    remaining_ingredients = all_ingredients - ingredients_containing_allergens
    count = sum(len(remaining_ingredients.intersection(i)) for i, _ in foods)
    return count

assert solve1(EXAMPLE) == 5

with open('input') as f:
    input = f.read()
print(solve1(input))
