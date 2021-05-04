import pandas as pd
import numpy as np

from readfile import readfile
from neighborhoods import main

# Read file
df, costs = readfile('scp41')

main(df, costs, 4, 8, 8, 0.75)
