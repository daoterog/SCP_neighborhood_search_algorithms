import pandas as pd
import numpy as np

def LS(df, costs, neigh, n = 2, n1 = 10, n2 = 10, alpha = 0.3, nsol):

    """
    Initialize nsol local search and chooses the one with the best results.

    Args:
        df: Dataframe that specifies which subset cover which elements 
        costs: costs of choosing each subset
        neigh: number that indicates which neighborhood to head
        n: n condition for second neighborhood
        n1: n condition for third neighborhood
        n2: n condition for fourth neighborhood
        alpha: percentage of the top half subsets that will be considered
        nsol: number of iterations to run

    Output:
        subsets: newly chosen subsets
    """

    # Generate First Solution and calculate cost
    initial_subsets = solution_generator(df, costs)
    initial_cost = calculatecosts(initial_subsets, costs)

    # To store results
    zs = []
    subset_options = []

    for i in range(nsol):
        subsets_option = LS_neighborhoods(df, costs, initial_subsets, neigh, n, n1, n2, alpha)
        cost_option = calculatecosts(subsets_option, costs)

        zs.append(cost_option)
        subset_options.append(subsets_option)
    
    # Select minimum, if multiple, pick randomly
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return min_zs, subsets

def LS_neighborhoods(df, costs, subsets, neigh, n, n1, n2, alpha):

    """
    Method that initializes and performs the descent in the local search. It stops when it reaches
    a local optimum.

    Args:
        df: Dataframe that specifies which subset cover which elements 
        costs: costs of choosing each subset
        subsests: chosen subsets
        neigh: number that indicates which neighborhood to head
        n: n condition for second neighborhood
        n1: n condition for third neighborhood
        n2: n condition for fourth neighborhood
        alpha: 

    Output:
        subsets: newly chosen subsets
    """

    before = calculatecosts(subsets, costs)
    new = 0
    
    # Initialize Search
    while before > new:
        before = calculatecosts(subsets, costs)

        # Select Neigborhood
        if neigh == 1:
            subsets = F_S_neighborhood(df, costs, subsets, neigh = 1):

        elif neigh == 2:
            subsets = F_S_neighborhood(df, costs, subsets, neigh = 2, n):

        elif neigh == 3:
            subsets = third_neighborhood(df, costs, n1, subsets)

        else:
            subsets = fourth_neighborhood(df, costs, n2, alpha, substes)
        
        new =  calculatecosts(subsets, costs)
    
    return subsets