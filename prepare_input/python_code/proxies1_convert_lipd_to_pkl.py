#==============================================================================
# Load proxies, process them, and save the selected proxies.
#    author: Michael Erb
#    date  : 10/1/2025
#==============================================================================

import numpy as np
import lipd
import pickle

save_new_proxy_file = True


#%% LOAD DATA

# Load the proxy data
dir_proxies = 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
#proxies_all = lipd.readLipd(dir_proxies+'database/')
#proxies_all = lipd.readLipd(dir_proxies+'sample_100/')
proxies_all = lipd.readLipd(dir_proxies+'sample_1/')


#%% EXTRACT TIME SERIES

# Extract the time series
all_ts = lipd.extractTs(proxies_all)
#print(all_ts[0]['paleoData_TSid'])

#%% SAVE DATA

# Save the data to a pickle file
if save_new_proxy_file:
    output_filename = 'all_ts_dropbox_20251008.pkl'
    with open(dir_proxies+output_filename,'wb') as handle:
        pickle.dump(all_ts,handle,protocol=pickle.HIGHEST_PROTOCOL)


