import pandas as pd
import numpy as np

from neighborhoods import (solution_generator, FIFN, FISN, BIFN, BISN)
from auxiliaries import calculatecosts

def VND(df, costs):
    initial_solution_subsets = solution_generator(df, costs)
    initial_solution_cost = calculatecosts(initial_solution_subsets, costs)

    

