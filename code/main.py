import pandas as pd
import numpy as np
import time
import os

from readfile import readfile
from algorithms import VND, VNS, SA, LS

from auxiliaries import lowerbound, data

# File to read
root = os.path.join(os.getcwd(), 'datasets')
files = ['scp41', 'scp42', 'scpnrg1', 'scpnrg2', 'scpnrg3', 'scpnrg4', 
         'scpnrg5', 'scpnrh1', 'scpnrh2', 'scpnrh3', 'scpnrh4', 'scpnrh5']

# Parameters
nsol = 30 # Number of solutions suggested 
alpha1 = 0.5 # GRASP Parameters

# For the Simulated Anealing
T0 = 
Tf = 
L = 
r = 

# Results to dataframe
vnd_scores = [], vnd_nsub = [], vnd_subset = [], vnd_rel = [], vnd_times = []
sa_scores = [], sa_nsub = [], sa_subset = [], sa_rel = [], sa_times = []
ls_scores = [], ls_nsub = [], ls_subset = [], ls_rel = [], ls_times = []
lbound = [], nelements = [], nsubsets = []
means = ['Mean']

# The first two values printed on the list correspond to the total cost and
# the numbers of subsets chosen respectively
for name in files:

    # Read file
    df, costs = readfile(os.path.join(root, name + '.txt'))
    nelements.append(df.shape[0])
    nsubsets.append(df.shape[1])

    # Lower bound
    lb = lowerbound(df, costs)
    lbound.append(lb)

    # VND
    start_vnd = time.perf_counter()
    vnd_cost, vnd_subsets = VND(df, costs)
    time_vnd = time.perf_counter() - start_vnd
    print('C:\t',[vnd_cost,len(vnd_subsets)] + vnd_subsets,'\t',time_vnd)
    vnd_scores.append(vnd_cost)
    vnd_rel.append(np.float32(vnd_cost/lb), 3)
    vnd_times.append(np.float32(np.round(time_vnd,5)))
    vnd_nsub.append(len(vnd_subsets))
    vnd_subset.append(vnd_subsets)

    # SA
    start_sa = time.perf_counter()
    sa_cost, sa_subsets = SA(df, costs, T0, Tf, L, r, neigh = 4)
    time_sa = time.perf_counter() - start_sa
    print('C:\t',[sa_cost,len(sa_subsets)] + sa_subsets,'\t',time_sa)
    sa_scores.append(sa_cost)
    sa_rel.append(np.float32(sa_cost/lb), 3)
    sa_times.append(np.float32(np.round(time_sa,5)))
    sa_nsub.append(len(sa_subsets))
    sa_subset.append(sa_subsets)

    # LS
    start_ls = time.perf_counter()
    ls_cost, ls_subset = LS(df, costs, neigh = 4, nsol = 30)
    time_ls = time.perf_counter() - start_ls
    print('C:\t',[ls_cost,len(ls_subsets)] + ls_subsets,'\t',time_ls)
    ls_scores.append(ls_cost)
    ls_rel.append(np.float32(ls_cost/lb), 3)
    ls_times.append(np.float32(np.round(time_ls,5)))
    ls_nsub.append(len(ls_subsets))
    ls_subset.append(ls_subsets)

# Create dataframe
front_vnd = np.transpose([vnd_scores, vnd_nsub])
front_sa = np.transpose([sa_scores, sa_nsub])
front_ls = np.transpose([ls_scores, ls_nsub])
matrix_vnd, matrix_sa, matrix_ls = data(vnd_nsub, sa_nsub, ls_nsub, vnd_subset, sa_subset, ls_subset)
data_front_vnd = np.c_[front_vnd,matrix_vnd]
data_front_sa = np.c_[front_sa,matrix_sa]
data_front_ls = np.c_[front_ls,matrix_ls]

df_vnd = pd.DataFrame(data = data_front_vnd)
df_sa = pd.DataFrame(data = data_front_sa)
df_ls = pd.DataFrame(data = data_front_ls)

means = means + [np.mean(nelements), np.mean(nsubsets), np.mean(lb), np.mean(vnd_scores),
              np.mean(vnd_rel), np.mean(vnd_times), np.mean(sa_scores), np.mean(sa_rel),
              np.mean(sa_times), np.mean(ls_scores), np.mean(ls_rel), np.mean(ls_times)]

columns = ['Files', 'Elements', 'Subsets', 'LB', 'Scores_VND', 'Gap_VND', 'Time_VND', 
            'Scores_SA', 'Gap_SA', 'Time_SA', 'Scores_LS', 'Gap_LS', 'Time_LS']

last = dict(zip(columns, means))
dat = [files, nelements, nsubsets, lbound, vnd_scores, vnd_rel, vnd_times, sa_scores, sa_rel, 
        sa_times, ls_scores, ls_rel, ls_times]
results = pd.DataFrame(data = np.transpose(dat), columns = columns)
results = results.append(last, ignore_index = True)

# To excel
df_vnd.to_csv('SCP_DanielOtero_VND.csv', header = False, index = False)
df_sa.to_csv('SCP_DanielOtero_SA.csv', header = False, index = False)
df_ls.to_csv('SCP_DanielOtero_LS.csv', header = False, index = False)
results.to_csv('SCP_DanielOtero_comparison.csv', index = False)
