#==============================================================================
# Load proxies, process them, and save the selected proxies.
#    author: Michael Erb
#    date  : 10/1/2025
#==============================================================================

#TODO: Look at this: https://pylipd.readthedocs.io/en/latest/api.html

import sys
sys.path.append('C:/Users/erbm/Dropbox/Academia/NAU/Project_EcoClimate_Sensitivity/analysis/utils/')
import utils_ecoclimate as utils
import numpy as np
#import lipd
import pylipd
from pylipd.lipd import LiPD

#%% LOAD DATA

lipd = LiPD()
lipd.load('C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/sample_10/3cBx.Sagawa.2012.lpd')
ts_list = lipd.get_timeseries(lipd.get_all_dataset_names())
key = list(ts_list.keys())[0]
len(ts_list[key])

# Load the proxy data
dir_proxies = 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
proxies_all = lipd.readLipd(dir_proxies+'sample_10/')

# Extract the time series
all_ts = lipd.extractTs(proxies_all)
#print(all_ts[0]['paleoData_TSid'])

#%% OVERVIEW

utils.overview(all_ts,'paleoData_TSid',count_min=1)



# List metadata
utils.overview(all_ts,'archiveType',count_min=1)
utils.overview(all_ts,'paleoData_variableName',             count_min=1)


utils.overview(all_ts,'paleoData_interpretation_0_variable',count_min=1)
utils.overview(all_ts,'paleoData_primaryTimeseries',        count_min=1)
utils.overview(all_ts,'paleoData_units',                    count_min=1)

#%% FILTER

# Get records with a specific interpretation
selected_ts = []
for i in range(len(all_ts)):
    try:    variablename_record = all_ts[i]['paleoData_variableName']
    except: variablename_record = 'Not given'
    if (variablename_record == 'temperature'):
       selected_ts.append(all_ts[i])
