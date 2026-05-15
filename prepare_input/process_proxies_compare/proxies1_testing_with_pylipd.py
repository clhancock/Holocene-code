#==============================================================================
# Load proxies, process them, and save the selected proxies.
#    author: Michael Erb
#    date  : 10/1/2025
#==============================================================================

#TODO: Look at this: https://pylipd.readthedocs.io/en/latest/api.html
import numpy as np
import lipd
import pylipd
from pylipd.lipd import LiPD
import glob


#%% LOAD DATA - old lipd utilities

dir_proxies = 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/more/sample_1/'

# Load the proxy data
proxies_all_old = lipd.readLipd(dir_proxies)
all_ts_old = lipd.extractTs(proxies_all_old)
print('N proxies: ',len(proxies_all_old))
print('N timeseries: ',len(all_ts_old))


#%% LOAD DATA - new lipd utilities

# Load the proxy data
lipd = LiPD()
lipd_files = glob.glob(dir_proxies+'*')
lipd.load(lipd_files)
all_ts_new = lipd.get_timeseries(lipd.get_all_dataset_names())
key = list(all_ts_new.keys())[0]
all_ts_new = all_ts_new[key]


#%% COMPARE DATA STRUCTURES

print(len(all_ts_old))
print(len(all_ts_new))

print(all_ts_old[0].keys())
print(all_ts_new[0].keys())

