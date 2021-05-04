import pandas as pd
import numpy as np
import os

from readfile import readfile
from neighborhoods import main

root = 'datasets/'

# Read file
df, costs = readfile(os.path.join(root,'scp41'))

cost, subsets = VND(df, costs)
