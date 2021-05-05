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


def VND(df, costs, subsets = [], n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):

    initial_solution_subsets = []

    # Get initial solution
    if not subsets:
        initial_solution_subsets = solution_generator(df, costs)

    else:
        initial_solution_subsets = subsets

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

def VNS(df, costs, subsets = [], n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):
    
    initial_solution_subsets = []

    # Get initial solution
    if not subsets:
        initial_solution_subsets = solution_generator(df, costs)

    else:
        initial_solution_subsets = subsets

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

        # More Auxiliaries
        new_cost_before = new_cost
        new_subsets_before = new_subsets
        local_optimum = False

        # Check if it is a local optimum
        while not local_optimum:

            newc, newsub = find_neighborhoods(j, df, costs, new_subsets_before, n, n1, n2, alpha, nsol)
            print('New Solution: %s' % newc)

            if newc < new_cost_before:

                new_cost_before = newc
                new_subsets_before = newsub
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

def SA(df, costs, T0, Tf, L, r, j = 3, n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol = 30):

    # Get initial solution
    initial_solution_subsets = solution_generator(df, costs)
    initial_solution_cost = calculatecosts(initial_solution_subsets, costs)

    print('Initial Solution: %s' % initial_solution_cost)

    # Initialize T
    T = T0

    # Aux
    cost_before = initial_solution_cost
    subsets_before = initial_solution_subsets

    # Start Loop
    while T > Tf:
        l = 0 

        # Start second Loop
        while l < L:
            l += 1
            new_cost = 0
            new_subsets = []

            if j < 5:

                # Find solution that belongs to the j neighborhood
                new_cost, new_subsets = find_neighborhoods(j, df, costs, subsets_before, n, n1, n2, alpha, nsol)
                print('New Solution: %s' % new_cost)

            elif j < 6:

                # Use VND
                new_cost, new_subsets = VND(df, costs, subsets_before)
                print('New Solution: %s' % new_cost)
            
            else:

                # Use VNS
                new_cost, new_subsets = VNS(df, costs, subsets_before)
                print('New Solution: %s' % new_cost)

            d = new_cost - cost_before

            if d < 0:

                # Update solution
                cost_before = new_cost
                subsets_before = new_subsets
                print('NEW IMPROVEMENT')
            
            else:
                rand = np.random.uniform(0,1)
                print(rand)
                print(np.exp(-d/T))

                if rand < np.exp(-d/T):

                    # Update solution
                    cost_before = new_cost
                    subsets_before = new_subsets
                    print('SET BACK')
        
        T = r*T

    print('Final Solution: %s' % cost_before)

    return cost_before, subsets_before

