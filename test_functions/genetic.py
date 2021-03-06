from random import randint, uniform
from functions import drop_wave, shubert


MAX_X1 = 5.12
MAX_X2 = 5.12

POPULATION_SIZE = 100
SOLUTIONS_TO_KEEP_IN_POPULATION = 50

MAX_ITERATIONS = 1000


def genetic(function):
    iteration = 0
    
    population = generate_initial_population()
    values = []
    
    while iteration < MAX_ITERATIONS:
        # calculate result value for each solution in population
        values = apply_function(population, function)
        
        # filter best solutions in population, reproduce and mutate
        population = choose_best_solutions(population, values)
        population = generate_descendants(population)
        population = mutate(population)
        
        iteration += 1
    
    best = find_best_solution(population, values)
    
    return best


def generate_initial_population():
    population = []
    
    for i in range(0, POPULATION_SIZE - 1):
        x1 = uniform(0, MAX_X1)
        x2 = uniform(0, MAX_X2)
        
        new_item = (x1, x2)
        
        population.append(new_item)
        
    return population

def apply_function(population, function):
    values = []
    
    for item in population:
        v = function(item[0], item[1])
        values.append(v)
        
    return values

def choose_best_solutions(population, values):
    top_population = []
    
    for i in range(0, SOLUTIONS_TO_KEEP_IN_POPULATION):
        best = find_best_solution(population, values)
        
        population.remove(best[0])
        values.remove(best[1])
        
        top_population.append(best[0])
        
    return top_population

def generate_descendants(population):
    number_of_descendants_to_create = POPULATION_SIZE - SOLUTIONS_TO_KEEP_IN_POPULATION
    
    for i in range(0, number_of_descendants_to_create):
        parents = choose_random_parents(population)
        
        child = reproduce(parents)
        
        population.append(child)
    
    return population

def choose_random_parents(population):
    index0 = randint(0, SOLUTIONS_TO_KEEP_IN_POPULATION - 1)
    index1 = randint(0, SOLUTIONS_TO_KEEP_IN_POPULATION - 1)
    
    return [population[index0], population[index1]]

def reproduce(parents):
    parent0 = parents[0]
    parent1 = parents[1]
    
    # calculates mean of parents x1 and x2
    x1 = (parent0[0] + parent1[0]) / 2
    x2 = (parent0[1] + parent1[1]) / 2
    
    return (x1, x2)

def mutate(population):
    for i in range(0, len(population)):
        probability_to_mutate = randint(1,10)
        
        # 30 % chance to mutate
        if probability_to_mutate > 7:
            # randomize the variable that will change value (0 => x1 and 1 => x2)
            index = randint(0,1)
            
            # add a random value between -1 and 1
            number_to_add = uniform(-1,1)
            
            # convert to list cause tuples can't be reassigned
            variables_list = list(population[i])
            variables_list[index] += number_to_add
            
            # make sure values are in the valid interval [-5.12, 5.12]
            if variables_list[index] > 5.12:
                variables_list[index] = 5.12
            elif variables_list[index] < -5.12:
                variables_list[index] = -5.12
                
            # convert back to tuple
            population[i] = tuple(variables_list)
        
    return population
    
def find_best_solution(population, values):
    best_value = values[0]
    best_solution = population[0]
    
    for i in range(0, len(values)):
        if values[i] < best_value:
            best_value = values[i]
            best_solution = population[i]
        
    return [best_solution, best_value]

# example usage:
# result = genetic(shubert)
#
# best_solution = result[0]
# best_value = result[1]
#
# print("\nMelhor resultado:{}\nx1 = {}\nx2 = {}".format(best_value, best_solution[0], best_solution[1]))
