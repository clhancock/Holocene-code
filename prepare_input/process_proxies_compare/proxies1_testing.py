#==============================================================================
# Load proxies, process them, and save the selected proxies.
#    author: Michael Erb
#==============================================================================

import sys
sys.path.append('C:/Users/erbm/Dropbox/Academia/NAU/Project_EcoClimate_Sensitivity/analysis/utils/')
import numpy as np
import lipd
import utils_ecoclimate as utils

#%% LOAD DATA

# Load the proxy data
dir_proxies = 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
#proxies_all = lipd.readLipd(dir_proxies+'database/')
#proxies_all = lipd.readLipd(dir_proxies+'sample_100/')
#proxies_all = lipd.readLipd(dir_proxies+'sample_1/')
#proxies_all = lipd.readLipd(dir_proxies+'sample_10/')
proxies_all = lipd.readLipd(dir_proxies+'sample_new/')
all_ts = lipd.extractTs(proxies_all)
print('N proxies: ',len(proxies_all))
print('N timeseries: ',len(all_ts))

#%% OVERVIEW

# List metadata
utils.overview(all_ts,'dataSetName',count_min=1)
utils.overview(all_ts,'paleoData_TSid',count_min=1)
utils.overview(all_ts,'paleoData_isPrimary',count_min=1)

all_ts[0]['paleoData_TSid']
all_ts[0]['paleoData_isPrimary']


#%% GET ALL DATABASE NAMES

selected_ts1 = []
for i in range(len(all_ts)):
    keys = list(all_ts[i].keys())
    if ('paleoData_values' in keys) and (('age' in keys) or ('year' in keys)):
        selected_ts1.append(all_ts[i])
    else:
        pass
        #print(i)

#TODO: Why do some records not include age, even though they seem to have age data, like i=1067
print('Filter 1 - time series has fields for paleoData_values and age or year')
print('Time series remaining:',len(selected_ts1))