import pandas as pd
import numpy as np

from neighborhoods import (solution_generator, FIFN, FISN, BIFN, BISN)
from auxiliaries import calculatecosts

def find_neighborhoods(j, df, costs, initial_solution_subsets, n, n1, n2, alpha, nsol):

    subsets = []
    cost = 0

    # Search in corresponding neighborhood
    if j == 1:
        cost, subsets = FIFN(df, costs, initial_solution_subsets, nsol)
    elif j == 2:
        cost, subsets = FISN(df, costs, n, initial_solution_subsets, nsol)
    elif j == 3:
        cost, subsets = BIFN(df, costs, n1, subsets_incial, nsol)
    else:
        cost, subsets = BISN(df, costs, n2, alpha, subsets_incial, nsol)

    return subsets, costs


def VND(df, costs, n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):

    # Get initial solution
    initial_solution_subsets = solution_generator(df, costs)
    initial_solution_cost = calculatecosts(initial_solution_subsets, costs)

    print('Initial Solution: %s' % initial_solution_cost)

    j = 0

    # Aux
    cost_before = initial_solution_cost
    subsets_before = initial_solution_cost

    # Start neighborhood search
    while j < 4:
        
        print(j)
        # Find solution that belongs to the j neighborhood
        new_cost, new_subsets = find_neighborhoods(j, df, costs, subsets_before, n, n1, n2, aplha, nsol)
        print('New Solution: %s' % new_cost)

        if new_cost < cost_before:
            j = 1

            # Update values
            cost_before = new_cost
            subsets_before = new_subsets

            print('NEW IMPROVEMENT')
        
        else:
            j += 1
    
    return final_cost, final_subsets




        

    

