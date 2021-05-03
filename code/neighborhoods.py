import pandas as pd
import numpy as np
import time

from auxiliaries import calculatecosts

def find_lower_cost_subsets(df, costs, reference_cost):
    df_copy1 = df.copy()
    costs_copy1 = costs.copy()

    # Define child evaluation statistics
    childs_costs = 0
    childs_elements = 0

    # Subset array
    subsets = []

    while childs_costs < reference_cost:

        # Create aux arrays
        nelements = df_copy1.sum()

        # Delete substes that no longer have elements
        no_elements = nelements[nelements == 0].index.tolist()
        if no_elements != []:
            df_copy1.drop(no_elements, axis = 1, inplace = True)
            costs_copy1.drop(no_elements, inplace = True)
            nelements = df_copy1.sum()
        
        # Breaking if there are no more elements to asign
        if df_copy1.empty:
            break

        # Extract random subset with minimum cost
        min_cost = costs_copy1.min()
        min_cost_subsets = costs_copy1[costs_copy1 == min_cost]
        indx_random_min_cost_subset = min_cost_subsets.sample(1).index[0]

        # Adding subset to list
        subsets.append(indx_random_min_cost_subset)

        # Extract number of elements that covers the lowest costing subset
        nelem_min_cost_subset = nelements[indx_random_min_cost_subset]

        # Sum cost and number of elements of the lowest costing subset
        childs_costs += min_cost
        childs_elements += nelem_min_cost_subset

        # Update df and costs by deleteing chosen subset
        # Extract all the elements contained in the subset and drop them according
        # to their index
        subset_elements = df_copy1[df_copy1[indx_random_min_cost_subset] == 1].index
        df_copy1.drop(subset_elements, axis = 0, inplace = True)
        df_copy1.drop(indx_random_min_cost_subset, axis = 1, inplace = True)
        costs_copy1.drop(indx_random_min_cost_subset, inplace = True)

    return subsets

def solution_generator(df, costs):
    df_copy = df.copy()
    costs_copy = costs.copy()

    # Subset array
    subsets = []

    while not df_copy.empty:

        # Create aux arrays
        nelements = df_copy.sum()

        # Delete substes that no longer have elements
        no_elements = nelements[nelements == 0].index.tolist()

        if no_elements != []:

            # Drop empty subsets
            df_copy.drop(no_elements, axis = 1, inplace = True)
            costs_copy.drop(no_elements, inplace = True)

            # Update nelements
            nelements = df_copy.sum()

        # Find maximum number of elements that a subset has
        maximum_element = nelements.max()

        # Find subsets that have the most elements and its costs
        nmax_subsets = nelements[nelements == maximum_element].index
        cost_nmax_subset = costs_copy[nmax_subsets]

        # Find subsets with minimum cost
        mincost = cost_nmax_subset.min()
        mincost_nmax_subsets = cost_nmax_subset[cost_nmax_subset == mincost]

        # Pick random
        mincost_subset_idx = mincost_nmax_subsets.sample(1).index[0]

        # Assign solution 
        subsets.append(mincost_subset_idx)

        # Update Dataframe
        # Extract all the elements contained in the subset and drop them according
        # to their index
        subset_elements = df_copy[df_copy[mincost_subset_idx] == 1].index
        df_copy.drop(subset_elements, axis = 0, inplace = True)
        df_copy.drop(mincost_subset_idx, axis = 1, inplace = True)
        costs_copy.drop(mincost_subset_idx, inplace = True)

    return subsets

def FIfirst_neighborhood(df, costs, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    # First Neighborhood
    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)
        print(subsets)
        print('Anterior: ' + str(anterior))

        # Copy df and costs to perform operations
        df_c1 = df.copy()
        costs_c1 = costs.copy()

        # Extract maximum cost subset
        subset_costs = costs_c1.iloc[subsets]
        max_cost = subset_costs.max()
        subsets_max_cost = subset_costs[subset_costs == max_cost].index.tolist()

        # Number lements that will be tried to cover with a lower cost
        subset_elements = 0

        # In the case that there are various subsets with the same cost
        # pick the one with the most elements
        if len(subsets_max_cost) != 1:
            nelements = df_c1.sum()
            nelem_subsets_max_cost = nelements.iloc[subsets_max_cost]
            subset_elements = nelem_subsets_max_cost.max()
            max_elements_subset = nelem_subsets_max_cost[nelem_subsets_max_cost == subset_elements]

            # Pick one randomly
            subsets_max_cost = max_elements_subset.sample(1).index[0]

        else:
            nelements = df_c1.sum()
            subset_elements = nelements.iloc[subsets_max_cost]
            subsets_max_cost = subsets_max_cost[0]

        # Instance new subset array
        cutted_subsets = [s for s in subsets if s!= subsets_max_cost]

        # Update Dataframe
        # Extract all the elements contained in the subset and drop them according
        # to their index
        subset_elements = df_c1[(df_c1[cutted_subsets] == 1).sum(axis = 1) >= 1].index
        df_c1.drop(subset_elements, axis = 0, inplace = True)
        df_c1.drop(cutted_subsets, axis = 1, inplace = True)
        costs_c1.drop(cutted_subsets, inplace = True)

        # If the DataFrame is empty then we could easily improve the solution,
        # if not, we improve it using the following funtcion
        if not df_c1.empty:
            replacement_subsets = find_lower_cost_subsets(df_c1, costs_c1, max_cost)

            if replacement_subsets:
                print('FUNCIONA')

                subsets_option = cutted_subsets + replacement_subsets
                evaluate = calculatecosts(subsets_option, costs)

                if evaluate < anterior:
                    nueva = evaluate
                    subsets = subsets_option
                    print('Nueva: ' + str(nueva))
                else:
                    break

            else:
                print('HPTA')
        else:
            print('VACIO')

            # Update subset list
            subsets = cutted_subsets
            nueva = calculatecosts(subsets, costs)
            print('Nueva: ' + str(nueva))

    return subsets

def FIsecond_neighborhood(df, costs, n, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)
        print(subsets)
        print('Anterior: ' + str(anterior))

        # Copy df and costs to perform operations
        df_c2 = df.copy()
        costs_c2 = costs.copy()

        # Extract the n maximum cost subset
        subset_costs = costs_c2.iloc[subsets]
        max_cost = subset_costs.nlargest(n)
        subsets_cost = max_cost.sum()
        subsets_max_cost = max_cost.index.tolist()

        # Number lements that will be tried to cover with a lower cost
        subset_elements = 0

        # Instance new subset array
        cutted_subsets = [s for s in subsets if  not s in subsets_max_cost]

        # Update Dataframe
        # Extract all the elements contained in the subset and drop them according
        # to their index
        subset_elements = df_c2[(df_c2[cutted_subsets] == 1).sum(axis = 1) >= 1].index
        df_c2.drop(subset_elements, axis = 0, inplace = True)
        df_c2.drop(cutted_subsets, axis = 1, inplace = True)
        costs_c2.drop(cutted_subsets, inplace = True)

        # If the DataFrame is empty then we could easily improve the solution,
        # if not, we improve it using the following funtcion
        if not df_c2.empty:
            replacement_subsets = find_lower_cost_subsets(df_c2, costs_c2, subsets_cost)

            if replacement_subsets:
                print('FUNCIONA')

                subsets_option = cutted_subsets + replacement_subsets
                evaluate = calculatecosts(subsets_option, costs)

                if evaluate < anterior:
                    nueva = evaluate
                    subsets = subsets_option
                    print('Nueva: ' + str(nueva))
                else:
                    break

            else:
                print('HPTA')

        else:
            print('VACIO')

            # Update subset list
            subsets = cutted_subsets
            nueva = calculatecosts(subsets, costs)

    return subsets

def BIfirst_neighborhood(df, costs, n1, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    # First Neighborhood
    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)
        print(subsets)
        print('Anterior: ' + str(anterior))

        # Copy df and costs to perform operations
        df_c1 = df.copy()
        costs_c1 = costs.copy()

        # Extract maximum cost subset
        subset_costs = costs_c1.iloc[subsets]
        max_cost = subset_costs.nlargest(n1)

        # To store results
        zs = []
        subset_options = []

        for subsets_max_cost in max_cost.index.tolist():
            
            # Copy df and costs in order to iterate over "previous" versions
            # not current tests
            df_c2 = df_c1.copy()
            costs_c2 = costs_c1.copy()

            # Extract cost of the subset taken into account
            cost = max_cost[subsets_max_cost]

            # Number lements that will be tried to cover with a lower cost
            nelements = df_c2.sum()
            subset_elements = nelements[subsets_max_cost]

            # Instance new subset array
            cutted_subsets = [s for s in subsets if s!= subsets_max_cost]

            # Update Dataframe
            # Extract all the elements contained in the subset and drop them according
            # to their index
            subset_elements = df_c2[(df_c2[cutted_subsets] == 1).sum(axis = 1) >= 1].index
            df_c2.drop(subset_elements, axis = 0, inplace = True)
            df_c2.drop(cutted_subsets, axis = 1, inplace = True)
            costs_c2.drop(cutted_subsets, inplace = True)

            # If the DataFrame is empty then we could easily improve the solution,
            # if not, we improve it using the following funtcion
            if not df_c2.empty:
                replacement_subsets = find_lower_cost_subsets(df_c2, costs_c2, cost)
                if replacement_subsets:
                    print('FUNCIONA')

                    # Calculate subset option and store it
                    subsets_option = cutted_subsets + replacement_subsets
                    nueva_option = calculatecosts(subsets_option, costs)

                    zs.append(nueva_option)
                    subset_options.append(subsets_option)
                else:
                    print('HPTA')
            else:
                print('VACIO')

                # Calculate subset option and store it
                subsets_option = cutted_subsets
                nueva_option = calculatecosts(subsets_option, costs)

                zs.append(nueva_option)
                subset_options.append(subsets_option)

        # Datatype conversions in order to make operations easier
        zs = pd.Series(zs)
        min_zs = zs.min()
        mins = zs[zs == min_zs]
        rand_min = mins.sample(1).index[0]

        # Update values
        if min_zs < anterior:
            subsets = subset_options[rand_min]
            nueva = min_zs
            print('Nueva: ' + str(nueva))
        else:
            break

    return subsets

def BIsecond_neighborhood(df, costs, n, alpha, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)
        print(subsets)
        print('Anterior: ' + str(anterior))

        # Copy df and costs to perform operations
        df_c2 = df.copy()
        costs_c2 = costs.copy()

        # Extract the toph half maximum cost subset
        subset_costs = costs_c2.iloc[subsets]
        sorted_subset_costs = subset_costs.sort_values()
        half = round(len(sorted_subset_costs)/2)
        top_half_subset_costs = sorted_subset_costs.iloc[half:]

        # To store results
        zs = []
        subset_options = []

        for i in range(n):

            # Copy df and costs in order to iterate over "previous" versions
            # not current tests
            df_c3 = df_c2.copy()
            costs_c3 = costs_c2.copy()

            # Generate random sample of top half maximum cost subset
            n_sample = round(len(top_half_subset_costs)*alpha)
            max_cost = top_half_subset_costs.sample(n_sample)
            subsets_cost = max_cost.sum()
            subsets_max_cost = max_cost.index.tolist()

            # Instance new subset array
            cutted_subsets = [s for s in subsets if  not s in subsets_max_cost]

            # Update Dataframe
            # Extract all the elements contained in the subset and drop them according
            # to their index
            subset_elements = df_c3[(df_c3[cutted_subsets] == 1).sum(axis = 1) >= 1].index
            df_c3.drop(subset_elements, axis = 0, inplace = True)
            df_c3.drop(cutted_subsets, axis = 1, inplace = True)
            costs_c3.drop(cutted_subsets, inplace = True)

            # If the DataFrame is empty then we could easily improve the solution,
            # if not, we improve it using the following funtcion
            if not df_c3.empty:
                replacement_subsets = find_lower_cost_subsets(df_c3, costs_c3, subsets_cost)

                if replacement_subsets:
                    print('FUNCIONA')

                    # Calculate subset option and store it
                    subsets_option = cutted_subsets + replacement_subsets
                    nueva_option = calculatecosts(subsets_option, costs)

                    zs.append(nueva_option)
                    subset_options.append(subsets_option)

                else:
                    print('HPTA')

            else:
                print('VACIO')
                
                # Calculate subset option and store it
                subsets_option = cutted_subsets
                nueva_option = calculatecosts(subsets_option, costs)

                zs.append(nueva_option)
                subset_options.append(subsets_option)
            
        # Datatype conversions in order to make operations easier
        zs = pd.Series(zs)
        min_zs = zs.min()
        mins = zs[zs == min_zs]
        rand_min = mins.sample(1).index[0]

        # Update values
        if min_zs < anterior:
            subsets = subset_options[rand_min]
            nueva = min_zs
            print('Nueva: ' + str(nueva))
        else:
            break

    return subsets

def BIFN(df, costs, n, subsets, nsol):

    # To store results
    zs = []
    subset_options = []

    for i in range(nsol):
        subsets = BIfirst_neighborhood(df, costs, n, subsets)
        actual = calculatecosts(subsets, costs)

        zs.append(actual)
        subset_options.append(subsets)
    
    # Select minimum, if multiple, pick randomly
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return min_zs, subsets

def BISN(df, costs, n, alpha, subsets, nsol):

    # To store results
    zs = []
    subset_options = []

    for i in range(nsol):
        subsets = BIsecond_neighborhood(df, costs, n, alpha, subsets)
        actual = calculatecosts(subsets, costs)

        zs.append(actual)
        subset_options.append(subsets)
    
    # Select minimum, if multiple, pick randomly
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return min_zs, subsets

def FIFN(df, costs, subsets, nsol):

    # To store results
    zs = []
    subset_options = []

    for i in range(nsol):
        subsets = FIfirst_neighborhood(df, costs, subsets)
        actual = calculatecosts(subsets, costs)

        zs.append(actual)
        subset_options.append(subsets)
    
    # Select minimum, if multiple, pick randomly
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return min_zs, subsets

def FISN(df, costs, n, subsets, nsol):

    # To store results
    zs = []
    subset_options = []

    for i in range(nsol):
        subsets = FIsecond_neighborhood(df, costs, n, subsets)
        actual = calculatecosts(subsets, costs)

        zs.append(actual)
        subset_options.append(subsets)
    
    # Select minimum, if multiple, pick randomly
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return min_zs, subsets

def main(df, costs, n, n1, n2, alpha, nsol):

    # Generate First Solution and calculate cost
    subsets_incial = solution_generator(df, costs)
    basica = calculatecosts(subsets_incial, costs)

    print('Solucion actual: ' + str(basica))

    # Best Improvement First Neighborhood
    print('PRIMER INTENTO')

    bifn_iter, bifn_subsets = BIFN(df, costs, n1, subsets_incial, nsol)

    print('Solucion actual: ' + str(bifn_iter))

    # Best Improvement First Neighborhood
    print('SEGUNDO INTENTO')

    bisn_iter, bisn_subsets = BISN(df, costs, n2, alpha, subsets_incial, nsol)

    print('Solucion actual: ' + str(bisn_iter))

    # First Improvement Second Neighborhood
    print('TERCER INTENTO')

    fisn_iter, fisn_subsets = FISN(df, costs, n, subsets_incial, nsol)

    print('Solucion actual: ' + str(fisn_iter))

    # First Improvement Second Neighborhood
    print('CUARTO INTENTO')

    fifn_iter, fifn_subsets = FIFN(df, costs, subsets_incial, nsol)

    print('QUINTO INTENTO')

    bifn_fifn_iter, bifn_fifn_subsets = BIFN(df, costs, n1, fifn_subsets, nsol)

    print('SEXTO INTENTO')
    bifn_fisn_iter, bifn_fisn_subsets = BIFN(df, costs, n1, fisn_subsets, nsol)

    print('SEPTIMO INTENTO')
    bifn_bisn_iter, bifn_bisn_subsets = BIFN(df, costs, n1, bisn_subsets, nsol)

    print('\n\n ITERACIONES')
    print(' BASICA: {0:d}\n BIFN: {1:d}\n BISN: '
    '{2:d}\n FISN: {3:d}\n FIFN: {4:d}\n FIFN-BIFN: {5:d}\n'
    ' FISN-BIFN: {6:d}\n BISN-BIFN: {7:d}'.format(basica, 
    bifn_iter, bisn_iter, fisn_iter, fifn_iter, bifn_fifn_iter, bifn_fisn_iter,
    bifn_bisn_iter))



    


    

    

    
    


    



