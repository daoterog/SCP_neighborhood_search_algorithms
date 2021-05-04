import pandas as pd
import numpy as np
import os

from readfile import readfile
from neighborhoods import main
from variable_neighborhoods import VND, VNS

root = os.path.join(os.getcwd(), 'datasets')

# Read file
df, costs = readfile(os.path.join(root, 'scp41.txt'))

cost, subsets = VNS(df, costs)

# main(df, costs, 2, 10, 10 , 0.3, 30)
