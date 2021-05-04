import pandas as pd 
import numpy as np

def lowerbound(df, costs):

    maxelements = df.sum().max()
    minsubsets = np.ceil(df.shape[0]/maxelements)

    mincost = costs.min()

    lb = mincost*minsubsets

    return lb

def calculatecosts(subsets, costs):
    z = 0

    for subset in subsets:
        z += costs[subset]

    return z

def data(c_nsub, g_nsub, n_nsub, c_subset, g_subset, n_subset):
    c_max = max(c_nsub)
    g_max = max(g_nsub)
    n_max = max(n_nsub)
    
    def_max = max([c_max, g_max, n_max])
    len_files = len(c_nsub)

    matrix_c = np.zeros((len_files, def_max))
    matrix_g = np.zeros((len_files, def_max))
    matrix_n = np.zeros((len_files, def_max))

    i = 0
    while i < len_files:
    
        # Extract subset constructive
        sub = c_subset[i]

        # Rewrite matrix
        for j in range(len(sub)):
            matrix_c[i][j] = sub[j]
            top = j
        for k in range(top, def_max):
            matrix_c[i][k] = None

        # Extract subset grasp
        sub = g_subset[i]

        # Rewrite matrix
        for j in range(len(sub)):
            matrix_g[i][j] = sub[j]
            top = j
        for k in range(top, def_max):
            matrix_g[i][k] = None

        # Extract subset noise
        sub = n_subset[i]

        # Rewrite matrix
        for j in range(len(sub)):
            matrix_n[i][j] = sub[j]
            top = j
        for k in range(top, def_max):
            matrix_n[i][k] = None
    
        i +=1

    return matrix_c, matrix_g, matrix_n