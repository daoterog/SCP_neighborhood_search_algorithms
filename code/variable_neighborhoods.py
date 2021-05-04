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
        cost, subsets = BIFN(df, costs, n1, initial_solution_subsets, nsol)
    else:
        cost, subsets = BISN(df, costs, n2, alpha, initial_solution_subsets, nsol)

    return cost, subsets


def VND(df, costs, n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):

    # Get initial solution
    initial_solution_subsets = solution_generator(df, costs)
    initial_solution_cost = calculatecosts(initial_solution_subsets, costs)

    print('Initial Solution: %s' % initial_solution_cost)

    # Aux
    j = 1
    cost_before = initial_solution_cost
    subsets_before = initial_solution_subsets

    # Start neighborhood search
    while j <= 4:
        
        print(j)
        # Find solution that belongs to the j neighborhood
        new_cost, new_subsets = find_neighborhoods(j, df, costs, subsets_before, n, n1, n2, alpha, nsol)
        print('New Solution: %s' % new_cost)

        if new_cost < cost_before:
            j = 1

            # Update values
            cost_before = new_cost
            subsets_before = new_subsets

            print('NEW IMPROVEMENT')
        
        else:
            j += 1

    print('Final Solution: %s' % cost_before)
    
    return cost_before, subsets_before

def VNS(df, costs, n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):
    
    # Get initial solution
    initial_solution_subsets = solution_generator(df, costs)
    initial_solution_cost = calculatecosts(initial_solution_subsets, costs)

    # Aux
    j = 1
    cost_before = initial_solution_cost
    subsets_before = initial_solution_subsets

    # Start neighborhood search
    while j <= 4:
        
        print(j)
        # Find solution that belongs to the j neighborhood
        new_cost, new_subsets = find_neighborhoods(j, df, costs, subsets_before, n, n1, n2, alpha, nsol)
        print('New Solution: %s' % new_cost)

        # More Auxiliaries
        new_cost_before = new_cost
        new_subsets_before = new_subsets
        local_optimum = False

        # Check if it is a local optimum
        while not local_optimum:

            newc, newsub = find_neighborhoods(j, df, costs, new_subsets_before, n, n1, n2, alpha, nsol)

            if newc < new_cost_before:

                new_cost_before = newc
                new_subsets_before = newsub
                print('New Solution: %s' % newc)
                print('NEW IMPROVEMENT')

            else:

                local_optimum = True
                print('LOCAL OPTIMUM')

        if new_cost_before < cost_before:
            cost_before = new_cost_before
            subsets_before = new_subsets_before
            j = 1

        else:
            j += 1

    print('Final Solution: %s' % cost_before)

    return cost_before, subsets_before

def SA(df, costs, n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):









        

    

