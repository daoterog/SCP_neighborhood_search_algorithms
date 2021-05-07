import pandas as pd
import numpy as np
import os

from readfile import readfile
# from neighborhoods import main
from variable_neighborhood import VND, VNS, SA

from local_search import LS

root = os.path.join(os.getcwd(), 'datasets')

# Read file
df, costs = readfile(os.path.join(root, 'scp41.txt'))

# cost, subset = LS(df, costs, 4, nsol = 10)

# cost, subsets = VND(df, costs)

# cost, subsets = VNS(df, costs)

cost, subsets = SA(df, costs, 90, 10, 5, 0.7, j = 3)

# main(df, costs, 2, 10, 10 , 0.3, 30)
