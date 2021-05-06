import pandas as pd
import numpy as np

def F_S_neighborhood(df, costs, subsets, neigh, n = 2):

    """
    Interface that connects with the way of extracting first and second neighborhood

    Args:
        df: Dataframe that specifies which subset cover which elements 
        costs: costs of choosing each subset
        subsests: chosen subsets

    Output:
        subsets: new chosen subsets
    """

    # Copy df and costs to perform operations
    df_copy = df.copy()
    costs_copy = costs.copy()

    # Aux
    subsets_max_cost = []

    # Decide which neighborhood structure to use
    if neigh == 1:
        subsets_max_cost = first_neighborhood(df, costs, subsets)
    else:
        subsets_max_cost = second_neighborhood(df, costs, n, subsets)

    # Instance new subset array
    cutted_subsets = [s for s in subsets if  not s in subsets_max_cost]

    # Update Dataframe
    # Extract all the elements contained in the subset and drop them according
    # to their index
    subset_elements = df_copy[(df_copy[cutted_subsets] == 1).sum(axis = 1) >= 1].index
    df_copy.drop(subset_elements, axis = 0, inplace = True)
    df_copy.drop(cutted_subsets, axis = 1, inplace = True)
    costs_copy.drop(cutted_subsets, inplace = True)

    # If the DataFrame is empty then we could easily improve the solution,
    # if not, we improve it using the following funtcion
    if not df_copy.empty:
        replacement_subsets = find_lower_cost_subsets(df_copy, costs_copy, max_cost)

        if replacement_subsets:
            # print('REPLACEMENT FOUND')

            subsets = cutted_subsets + replacement_subsets
        # else:
        #     print('REPLACEMENT NOT FOUNT')
    else:
        # print('NO REPLACEMENT NEEDED')

        subsets = cutted_subsets

    return subsets

def first_neighborhood(df, costs, subsets):

    """
    First way of iterating over a neighborhood. The method identifies the subset with
    with the maximum cost, if there are multiple it chooses the one that covers the most
    elements, if there is a tie then it chooses one randomly. Then the function 
    find_subset_set attemps to find a set of substes that cover the elements left 
    uncovered by the possible elimination of the chosen subset. 

    Args:
        df: Dataframe that specifies which subset cover which elements 
        costs: costs of choosing each subset
        subsests: chosen subsets

    Output:
        subsets: new chosen subsets
    """

    # Extract maximum cost subset
    subset_costs = costs.iloc[subsets]
    max_cost = subset_costs.max()
    subsets_max_cost = subset_costs[subset_costs == max_cost].index.tolist()

    # In the case that there are various subsets with the same cost
    # pick the one with the most elements
    if len(subsets_max_cost) != 1:
        nelements = df.sum()
        nelem_subsets_max_cost = nelements.iloc[subsets_max_cost]
        subset_max_elements = nelem_subsets_max_cost.max()
        max_elements_subset = nelem_subsets_max_cost[nelem_subsets_max_cost == subset_max_elements]

        # Pick one randomly
        subsets_max_cost = max_elements_subset.sample(1).index[0]

    else:
        subsets_max_cost = subsets_max_cost[0]

    return subsets_max_cost

def second_neighborhood(df, costs, n, subsets):

    """
    Second way of iterating through a neighborhood. The method identifies the subsets
    with the n largest costs and attemps to found a set of subsets that covers the elements
    left out if those subsets are not considered with the help of the find_subset_set function.

    Args:
        df: DataFrame that specifies which subset cover which elements 
        costs: costs of choosing each subset
        n: specifies the number of subsets considered
        subsests: chosen subsets

    Output:
        subsets: new chosen subsets
    """

    # Extract the n maximum cost subset
    subset_costs = costs_c2.iloc[subsets]
    max_cost = subset_costs.nlargest(n)
    subsets_cost = max_cost.sum()
    subsets_max_cost = max_cost.index.tolist()

    return subsets_max_cost

def third_neighborhood(df, costs, n, subsets):

    """
    Third way of iterating through the neighborhoods. This method takes the n subsets
    with the largest costs and attemps to find a set of of subsets that covers the elements
    left out when each of this subsets is not considered individually. The function then chooses
    to replace the subsets that lowers the most the cost function, if there is a tie it chooses randomly.

    Args:
        df: DataFrame that specifies which subset cover which elements 
        costs: costs of choosing each subset
        n: specifies the number of subsets considered
        subsests: chosen subsets

    Output:
        subsets: new chosen subsets
    """

    # Copy df and costs to perform operations
    df_c3 = df.copy()
    costs_c3 = costs.copy()

    # Extract maximum cost subset
    subset_costs = costs_c3.iloc[subsets]
    max_cost = subset_costs.nlargest(n)

    # To store results
    zs = []
    subset_options = []

    # Start loop
    for subsets_max_cost in max_cost.index.tolist():
            
        # Copy df and costs in order to iterate over "previous" versions
        # not current tests
        df_c31 = df_c3.copy()
        costs_c31 = costs_c3.copy()

        # Extract cost of the subset taken into account
        cost = max_cost[subsets_max_cost]

        # Instance new subset array
        cutted_subsets = [s for s in subsets if s!= subsets_max_cost]

        # Update Dataframe
        # Extract all the elements contained in the subset and drop them according
        # to their index
        subset_elements = df_c31[(df_c31[cutted_subsets] == 1).sum(axis = 1) >= 1].index
        df_c31.drop(subset_elements, axis = 0, inplace = True)
        df_c31.drop(cutted_subsets, axis = 1, inplace = True)
        costs_c31.drop(cutted_subsets, inplace = True)

        # If the DataFrame is empty then we could easily improve the solution,
        # if not, we improve it using the following funtcion
        if not df_c31.empty:
            replacement_subsets = find_lower_cost_subsets(df_c31, costs_c31, max_cost)

            if replacement_subsets:
                # print('REPLACEMENT FOUND')

                # Calculate subset option and store it
                subsets_option = cutted_subsets + replacement_subsets
                new_option = calculatecosts(subsets_option, costs)

                zs.append(new_option)
                subset_options.append(subsets_option)
            # else:
            #     print('REPLACEMENT NOT FOUNT')
        else:
            # print('NO REPLACEMENT NEEDED')

            # Calculate subset option and store it
            subsets_option = cutted_subsets + replacement_subsets
            new_option = calculatecosts(subsets_option, costs)

            zs.append(new_option)
            subset_options.append(subsets_option)

    # Datatype conversions in order to make operations easier
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return subsets

def fourth_neighborhood(df, costs, n, aplha, subsets):

    """
    Fourth way of iterating over a neighborhood. It first selects the top half subsets with higher
    costs. Then it runs n iterations in which a random sample of size alpha*len(tophalf) will be considered.
    The find_subset_set will be find a set of subsets that cover the elements left when not considering
    the random sample. Finally, after n iterations, it selects the one that minimizes the cost function, if
    there is a tie it selects one randomly.

    Args:
        df: DataFrame that specifies which subset cover which elements. 
        costs: costs of choosing each subset.
        n: specifies the number of subsets considered.
        alpha: percentage of the top half subsets that will be considered.
        subsests: chosen subsets.

    Output:
        subsets: new chosen subsets.
    """

    # Copy df and costs to perform operations
    df_c4 = df.copy()
    costs_c4 = costs.copy()

    # Extract the toph half maximum cost subset
    subset_costs = costs_c2.iloc[subsets]
    sorted_subset_costs = subset_costs.sort_values()
    half = round(len(sorted_subset_costs)/2)
    top_half_subset_costs = sorted_subset_costs.iloc[half:]

    for i in range(n):

        # Copy df and costs in order to iterate over "previous" versions
        # not current tests
        df_c41 = df_c4.copy()
        costs_c41 = costs_c4.copy()

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
        subset_elements = df_c41[(df_c41[cutted_subsets] == 1).sum(axis = 1) >= 1].index
        df_c41.drop(subset_elements, axis = 0, inplace = True)
        df_c41.drop(cutted_subsets, axis = 1, inplace = True)
        costs_c41.drop(cutted_subsets, inplace = True)

        # If the DataFrame is empty then we could easily improve the solution,
        # if not, we improve it using the following funtcion
        if not df_c41.empty:
            replacement_subsets = find_lower_cost_subsets(df_c41, costs_c41, max_cost)

            if replacement_subsets:
                # print('REPLACEMENT FOUND')

                # Calculate subset option and store it
                subsets_option = cutted_subsets + replacement_subsets
                new_option = calculatecosts(subsets_option, costs)

                zs.append(new_option)
                subset_options.append(subsets_option)
            # else:
            #     print('REPLACEMENT NOT FOUNT')
        else:
            # print('NO REPLACEMENT NEEDED')

            # Calculate subset option and store it
            subsets_option = cutted_subsets + replacement_subsets
            new_option = calculatecosts(subsets_option, costs)

            zs.append(new_option)
            subset_options.append(subsets_option)

    # Datatype conversions in order to make operations easier
    zs = pd.Series(zs)
    min_zs = zs.min()
    mins = zs[zs == min_zs]
    rand_min = mins.sample(1).index[0]

    subsets = subset_options[rand_min]

    return subsets

def BIsecond_neighborhood(df, costs, n, alpha, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)

        # print(subsets)
        # print('Anterior: ' + str(anterior))

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
                    # print('FUNCIONA')

                    # Calculate subset option and store it
                    subsets_option = cutted_subsets + replacement_subsets
                    nueva_option = calculatecosts(subsets_option, costs)

                    zs.append(nueva_option)
                    subset_options.append(subsets_option)

            else:
                # print('VACIO')
                
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

            # print('Nueva: ' + str(nueva))
        else:
            break

    return subsets

def BIfirst_neighborhood(df, costs, n1, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    # First Neighborhood
    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)

        # print(subsets)
        # print('Anterior: ' + str(anterior))

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
                    # print('FUNCIONA')

                    # Calculate subset option and store it
                    subsets_option = cutted_subsets + replacement_subsets
                    nueva_option = calculatecosts(subsets_option, costs)

                    zs.append(nueva_option)
                    subset_options.append(subsets_option)

            else:
                # print('VACIO')

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

            # print('Nueva: ' + str(nueva))
        else:
            break

    return subsets

def FIsecond_neighborhood(df, costs, n, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)

        # print(subsets)
        # print('Anterior: ' + str(anterior))

        # Copy df and costs to perform operations
        df_c2 = df.copy()
        costs_c2 = costs.copy()

        # Extract the n maximum cost subset
        subset_costs = costs_c2.iloc[subsets]
        max_cost = subset_costs.nlargest(n)
        subsets_cost = max_cost.sum()
        subsets_max_cost = max_cost.index.tolist()

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
                # print('FUNCIONA')

                subsets_option = cutted_subsets + replacement_subsets
                evaluate = calculatecosts(subsets_option, costs)

                if evaluate < anterior:
                    nueva = evaluate
                    subsets = subsets_option

                    # print('Nueva: ' + str(nueva))
                else:
                    break

        else:
            # print('VACIO')

            # Update subset list
            subsets = cutted_subsets
            nueva = calculatecosts(subsets, costs)

    return subsets

def FIfirst_neighborhood(df, costs, subsets):
    anterior = calculatecosts(subsets, costs)
    nueva = 0

    # First Neighborhood
    while anterior > nueva:
        anterior = calculatecosts(subsets, costs)

        # print(subsets)
        # print('Anterior: ' + str(anterior))

        # Copy df and costs to perform operations
        df_c1 = df.copy()
        costs_c1 = costs.copy()

        # Extract maximum cost subset
        subset_costs = costs_c1.iloc[subsets]
        max_cost = subset_costs.max()
        subsets_max_cost = subset_costs[subset_costs == max_cost].index.tolist()

        # In the case that there are various subsets with the same cost
        # pick the one with the most elements
        if len(subsets_max_cost) != 1:
            nelements = df_c1.sum()
            nelem_subsets_max_cost = nelements.iloc[subsets_max_cost]
            subset_max_elements = nelem_subsets_max_cost.max()
            max_elements_subset = nelem_subsets_max_cost[nelem_subsets_max_cost == subset_max_elements]

            # Pick one randomly
            subsets_max_cost = max_elements_subset.sample(1).index[0]

        else:
            nelements = df_c1.sum()
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
                # print('FUNCIONA')

                subsets_option = cutted_subsets + replacement_subsets
                evaluate = calculatecosts(subsets_option, costs)

                if evaluate < anterior:
                    nueva = evaluate
                    subsets = subsets_option

                    # print('Nueva: ' + str(nueva))
                else:
                    break

        else:
            # print('VACIO')

            # Update subset list
            subsets = cutted_subsets
            nueva = calculatecosts(subsets, costs)

            # print('Nueva: ' + str(nueva))

    return subsets


def LS_FIFN(df, costs, subsets, nsol):

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