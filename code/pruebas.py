import pandas as pd
import numpy as np
import os

from readfile import readfile
from algorithms import VND, VNS, SA, LS
from auxiliaries import lowerbound

root = os.path.join(os.getcwd(), 'datasets')

# Read file
df, costs = readfile(os.path.join(root, 'scp41.txt'))

# cost, subset = LS(df, costs, 4, nsol = 10)

# cost, subsets = VND(df, costs)

# cost, subsets = VNS(df, costs)

cost, subsets = SA(df, costs, 90, 30, 5, 0.9, neigh = 4)

# main(df, costs, 2, 10, 10 , 0.3, 30)
