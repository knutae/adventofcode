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

def solve2(input):
    foods = parse(input)
    all_allergens = set.union(*(set(allergens) for _, allergens in foods))
    all_ingredients = set.union(*(set(ingredients) for ingredients, _ in foods))
    ingredients_per_allergen = {
        allergen: ingredients_possibly_containing_allergen(foods, allergen)
        for allergen in all_allergens
    }
    while any(len(ingredients) > 1 for ingredients in ingredients_per_allergen.values()):
        removals = 0
        for allergen, ingredients in ingredients_per_allergen.items():
            if len(ingredients) == 1:
                # eliminate this ingredient from all other values
                ingredient = next(iter(ingredients))
                #print(f'Eliminating ingredient {ingredient} from others')
                for other_ingredients in ingredients_per_allergen.values():
                    if len(other_ingredients) > 1 and ingredient in other_ingredients:
                        other_ingredients.remove(ingredient)
                        removals += 1
        assert removals > 0
    #print(ingredients_per_allergen)
    result = [next(iter(ingredients_per_allergen[a])) for a in sorted(ingredients_per_allergen.keys())]
    #print(result)
    return ','.join(result)

assert solve2(EXAMPLE) == 'mxmxvkd,sqjhc,fvjkl'

with open('input') as f:
    input = f.read()
print(solve1(input))
print(solve2(input))
