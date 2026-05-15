#==============================================================================
# Load proxies and process them to only have proxies relavant for the
# EcoClimate project.
#    author: Michael Erb
#    date  : 2/18/2025
#==============================================================================

import sys
sys.path.append('C:/Users/erbm/Dropbox/Academia/NAU/Project_EcoClimate_Sensitivity/analysis/utils/')
import numpy as np
import pickle
import utils_ecoclimate as utils

save_new_proxy_file = False


#%% LOAD DATA

file_txt = 'all_ts_dropbox_20251008_basic'

# Load the proxy data
dir_proxies = 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/data_files_python/'
file_to_open = open(dir_proxies+file_txt+'.pkl','rb')
proxy_ts = pickle.load(file_to_open)
file_to_open.close()

# Any other filtering
print('Number of records total:',len(proxy_ts))
utils.overview(proxy_ts,'archiveType',count_min=1)
utils.overview(proxy_ts,'paleoData_primaryTimeseries',count_min=1)


"""
# Loop through the proxies, saving metadata.
proxies_borehole = []
for i in range(len(proxy_ts)):
    archiveType = proxy_ts[i]['archiveType']
    dataSetName = proxy_ts[i]['dataSetName']
    if (archiveType == 'TerrestrialSediment') & (dataSetName == 'BiggsvilleCessfordQuarry.Baker.1989'):
        proxies_borehole.append(proxy_ts[i])

print(' === GETTING PROXIES IN NORTH AMERICA ===')
print('Records remaining:',len(proxies_borehole))

utils.overview(proxies_borehole,'dataSetName',count_min=1)
utils.overview(proxies_borehole,'paleoData_TSid',count_min=1)
"""



#%% CHECK PROXY LONS

# Check proxy lons
proxy_lons = []
for i in range(len(proxy_ts)):
    proxy_lon = proxy_ts[i]['geo_meanLon']
    proxy_lons.append(proxy_lon)

print(min(proxy_lons),max(proxy_lons))  # Checking the proxy lons


#%% FILTER 1 - GET PROXIES IN SELECTED REGION

# Set the region. Note: the proxy lons are typically (always?) between -180 and 180
#region_bounds = [-170,-45,10,75]  # A tighter region
region_bounds = [-180,-10,0,85]  # A broader region that also encompasses Greenland

# Loop through the proxies, saving metadata.
proxies_in_region = []
for i in range(len(proxy_ts)):
    proxy_lat = proxy_ts[i]['geo_meanLat']
    proxy_lon = proxy_ts[i]['geo_meanLon']
    if (proxy_lon >= region_bounds[0]) & (proxy_lon <= region_bounds[1]) & (proxy_lat >= region_bounds[2]) & (proxy_lat <= region_bounds[3]):
        proxies_in_region.append(proxy_ts[i])

print(' === GETTING PROXIES IN NORTH AMERICA ===')
print('Records remaining:',len(proxies_in_region))

# List metadata
#utils.overview(proxies_in_region,'archiveType',                        count_min=1)
#utils.overview(proxies_in_region,'paleoData_interpretation_0_variable',count_min=1)
#utils.overview(proxies_in_region,'paleoData_variableName',             count_min=10)
#utils.overview(proxies_in_region,'paleoData_proxy',                    count_min=1)
#utils.overview(proxies_in_region,'paleoData_primaryTimeseries',        count_min=1)
#utils.overview(proxies_in_region,'paleoData_units',                    count_min=1)


#%% FILTER 2 - REMOVE POLLEN AND MIDDENS

# Get records that aren't pollen
selected_ts = []
for i in range(len(proxies_in_region)):
    try:    proxytype = proxies_in_region[i]['paleoData_proxy']
    except: proxytype = 'Not given'
    archivetype = proxies_in_region[i]['archiveType']
    if ((str(proxytype).lower() not in ['pollen']) & (str(archivetype).lower() not in ['midden'])):
        selected_ts.append(proxies_in_region[i])

print(' === REMOVING POLLEN AND MIDDENS ===')
print('Records remaining:',len(selected_ts))

#TODO: Lots of the remaining proxies don't seem to be useful. Figure out a better filter to get rid of them.
utils.overview(selected_ts,'paleoData_interpretation_0_variable',count_min=1)
utils.overview(selected_ts,'archiveType',count_min=1)


#%% FILTER 3 - GET TEMPERATURE AND PRECIPITION RECORDS

# Create a simplified interpretation variable
interp_temp   = ['temperature']
interp_precip = ['effectivePrecipitation','precipitation','hydrologicBalance']
for i in range(len(selected_ts)):
    try:    interp = selected_ts[i]['paleoData_interpretation'][0]['variable']
    except: interp = 'Not given'
    if   interp in interp_temp:   selected_ts[i]['interpSimple'] = 'temp'
    elif interp in interp_precip: selected_ts[i]['interpSimple'] = 'precip'
    elif interp == 'Not given':   selected_ts[i]['interpSimple'] = 'not_given'
    else:                         selected_ts[i]['interpSimple'] = 'other'

#utils.overview(selected_ts,'paleoData_units',count_min=1)

selected_ts_temp_precip = []
for i in range(len(selected_ts)):
    interp_simple = selected_ts[i]['interpSimple']
    if interp_simple in ['temp','precip']:
        selected_ts_temp_precip.append(selected_ts[i])

print(' === SELECTING TEMPERATURE AND PRECIPITATION ===')
print('Records remaining:',len(selected_ts_temp_precip))

utils.overview(selected_ts_temp_precip,'archiveType',count_min=1)
utils.overview(selected_ts_temp_precip,'paleoData_units',count_min=1)


#%% FILTER 4 - REMOVE WOOD
"""
# Remove wood, since it too short to be useful
selected_ts_without_wood = []
for i in range(len(selected_ts_temp_precip)):
    archivetype = selected_ts_temp_precip[i]['archiveType']
    if str(archivetype).lower() not in ['wood']:
        selected_ts_without_wood.append(selected_ts_temp_precip[i])

print(' === REMOVING WOOD ===')
print('Records remaining:',len(selected_ts_without_wood))
"""

#%% FILTER 5 - REMOVE RECORDS LESS THAN X YEARS OR WITHOUT VALID DATA

# Find a particular record
#for i in range(len(selected_ts_temp_precip)):
#    if selected_ts_temp_precip[i]['paleoData_TSid'] == "WEBb68390ad": print(i)

# Remove short records
selected_ts_long = []
record_length_all = []
for i in range(len(selected_ts_temp_precip)):
    #
    keys = list(selected_ts_temp_precip[i].keys())
    if 'paleoData_values' in keys:
        proxy_values = np.array(selected_ts_temp_precip[i]['paleoData_values']).astype(float)
    else:
        print(' --- WARNING: No paleoData_values in index',i,' SKIPPING ---')
        continue
    #
    # Get proxy time
    if 'age' in keys:
        proxy_ages = np.array(selected_ts_temp_precip[i]['age']).astype(float)
    elif 'year' in keys:
        #print(' --- WARNING: No ages in index',i,'---')
        proxy_years = np.array(selected_ts_temp_precip[i]['year']).astype(float)
        proxy_ages = 1950 - proxy_years
    else:
        print(' --- WARNING: No ages or years in index',i,' SKIPPING ---')
        continue
    #
    # Get valid data
    ind_valid = np.isfinite(proxy_values) & np.isfinite(proxy_ages)
    proxy_ages_valid = proxy_ages[ind_valid]
    if len(proxy_ages_valid) == 0:
        print(' --- WARNING: No valid data in index',i,' SKIPPING ---')
        continue
    #
    # Compute record lengths
    record_length = np.nanmax(proxy_ages_valid) - np.nanmin(proxy_ages_valid)
    record_length_all.append(record_length)
    #
    if record_length >= 2500:
        selected_ts_long.append(selected_ts_temp_precip[i])

print(' === REMOVING SHORT RECORDS ===')
print('Records remaining:',len(selected_ts_long))

#import matplotlib.pyplot as plt
#bins = np.arange(0,50001,2000)
#plt.hist(record_length_all,bins=bins)


#%% FILTER 6 - REMOVE RECORDS THAT DO NOT SEEM TO BE RIGHT

#TODO: Why is the MD02-2499.Lopez.2018 record here? Why wasn't it filtered out?
#TODO: Make this more general to catch strange records.

tsids_to_exclude = ['WEB33ffbfb3']  # Record MD02-2499.Lopez.2018

# Remove short records
selected_ts_without_some = []
for i in range(len(selected_ts_long)):
    proxy_tsid = selected_ts_long[i]['paleoData_TSid']
    if proxy_tsid in tsids_to_exclude: print(i,proxy_tsid)
    else: selected_ts_without_some.append(selected_ts_long[i])

print(' === REMOVING SELECTED RECORDS ===')
print('Records remaining:',len(selected_ts_without_some))


#%% FILTER - ONLY GET PROXIES IN SELECTED UNITS
"""
useful_units = ['degC','m','cm','mm','mm/yr','cm/yr','g/cm2/yr']

# Get records in units of 
selected_ts_units = []
for i in range(len(selected_ts_temp_precip)):
    try:    units = selected_ts_temp_precip[i]['paleoData_units']
    except: units = 'Not given'
    if (units in useful_units):
        selected_ts_units.append(selected_ts_temp_precip[i])

print(' === SELECTING USEFUL UNITS ===')
print('Records remaining:',len(selected_ts_units))

# List metadata
utils.overview(selected_ts_units,'paleoData_interpretation_0_variable',count_min=1)
utils.overview(selected_ts_units,'paleoData_variableName',             count_min=10)
utils.overview(selected_ts_units,'paleoData_primaryTimeseries',        count_min=1)
utils.overview(selected_ts_units,'paleoData_units',                    count_min=1)
"""


#%% SAVE DATA

# Save the data to a pickle file
if save_new_proxy_file:
    output_filename = file_txt+'_temp_precip_filtered.pkl'
    with open(dir_proxies+output_filename,'wb') as handle:
        pickle.dump(selected_ts_without_some,handle,protocol=pickle.HIGHEST_PROTOCOL)


