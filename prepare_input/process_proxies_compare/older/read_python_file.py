#==============================================================================
# A function to be used by R to read a pickle file
# From: https://stackoverflow.com/questions/58472090/loading-pickle-in-r
#    date  : 10/1/2025
#==============================================================================

import pandas as pd

def read_pickle(file_txt):
    file_data = pd.read_pickle(file_txt)
    return file_data

