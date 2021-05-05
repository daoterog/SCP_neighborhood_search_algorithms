import pandas as pd
import numpy as np
import os

from readfile import readfile
from neighborhoods import main
from variable_neighborhoods import VND, VNS, SA

root = os.path.join(os.getcwd(), 'datasets')

# Read file
df, costs = readfile(os.path.join(root, 'scp41.txt'))

# cost, subsets = VND(df, costs)

# cost, subsets = VNS(df, costs)

cost, subsets = SA(df, costs, 90, 10, 5, 0.7, j = 4)

# main(df, costs, 2, 10, 10 , 0.3, 30)
