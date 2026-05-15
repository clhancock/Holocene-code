#==============================================================================
# Load proxies, process them, and save the selected proxies.
#    author: Michael Erb
#    date  : 10/1/2025
#==============================================================================

import sys
sys.path.append('C:/Users/erbm/Dropbox/Academia/NAU/Project_EcoClimate_Sensitivity/analysis/utils/')
import numpy as np
import pickle
import utils_ecoclimate as utils

save_new_proxy_file = False
file_txt = 'all_ts_dropbox_20251008'
exp_txt  = 'basic'


#%% LOAD DATA

print(' ===== STARTING. file: '+file_txt+' =====')

# Load the proxy data
dir_proxies = 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/data_files_python/'
file_to_open = open(dir_proxies+file_txt+'.pkl','rb')
all_ts = pickle.load(file_to_open)
file_to_open.close()


#%% OVERVIEW

# List metadata
utils.overview(all_ts,'paleoData_interpretation_0_variable',count_min=1)
utils.overview(all_ts,'paleoData_variableName',             count_min=10)
utils.overview(all_ts,'paleoData_primaryTimeseries',        count_min=1)
utils.overview(all_ts,'paleoData_units',                    count_min=1)


#%% FILTER 1

print(' === TIMESERIES IN THE DATATBASE:',len(all_ts),'===')
print('Beginning filters')

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


#%% FILTER 2

# Get records with a specific interpretation
vars_to_exclude = ['age','depth','year']
interp_all       = []
variablename_all = []
primaryts_all    = []
selected_ts2     = []
for i in range(len(selected_ts1)):
    try:    primaryts = selected_ts1[i]['paleoData_primaryTimeseries']
    except: primaryts = 'Not given'
    try:    variablename_record = selected_ts1[i]['paleoData_variableName']
    except: variablename_record = 'Not given'
    try:    interp_record = selected_ts1[i]['paleoData_interpretation'][0]['variable']
    except: interp_record = 'Not given'
    interp_all.append(interp_record)
    variablename_all.append(variablename_record)
    primaryts_all.append(primaryts)
    if (str(primaryts).lower() not in ['false']) and \
       ('uncertainty' not in variablename_record.lower()) and \
       ('age-' not in variablename_record.lower()) and \
       (variablename_record.lower() not in vars_to_exclude):
       selected_ts2.append(selected_ts1[i])

#utils.print_sorted_list(interp_all,      'paleoData_interpretation_0_variable',count_min=1)
utils.print_sorted_list(variablename_all,'paleoData_variableName',             count_min=10)
#utils.print_sorted_list(primaryts_all,   'paleoData_primaryTimeseries',        count_min=1)

print('Filter 2 - primaryTimeseries is not False and var is not uncertainty, age, year, or depth')
print('Time series remaining:',len(selected_ts2))


#%% LOOK FOR RECORDS
"""
# Get records with a specific interpretation
selected_ts3 = []
for i in range(len(selected_ts2)):
#for i in range(100):
    try:    interp_record = selected_ts2[i]['paleoData_interpretation'][0]['variable']
    except: interp_record = 'Not given'
    if interp_record == 'Not given':
       #print(i)
       selected_ts3.append(selected_ts2[i])

utils.overview(selected_ts3,'paleoData_variableName',             count_min=1)
utils.overview(selected_ts3,'paleoData_variableName',             count_min=10)
"""
#%% LIST METADATA FOR SELECTED PROXIES

# List metadata
utils.overview(selected_ts2,'paleoData_interpretation_0_variable',count_min=1)
utils.overview(selected_ts2,'paleoData_variableName',             count_min=10)
utils.overview(selected_ts2,'paleoData_primaryTimeseries',        count_min=1)
utils.overview(selected_ts2,'paleoData_units',                    count_min=1)


#%% SAVE DATA

# Save the data to a pickle file
if save_new_proxy_file:
    output_filename = file_txt+'_'+exp_txt+'.pkl'
    with open(dir_proxies+output_filename,'wb') as handle:
        pickle.dump(selected_ts2,handle,protocol=pickle.HIGHEST_PROTOCOL)


