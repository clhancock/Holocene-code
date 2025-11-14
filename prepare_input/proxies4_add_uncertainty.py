#==============================================================================
# Add uncertainty values for proxies without values.
#    author: Michael P. Erb
#    date  : 11/6/2025
#==============================================================================

import sys
sys.path.append('C:/Users/erbm/Documents/GitHub/Holocene-code/')
sys.path.append('C:/Users/erbm/Dropbox/Academia/NAU/Project_EcoClimate_Sensitivity/analysis/utils/')
import numpy as np
import pickle
import da_utils
import utils_ecoclimate as utils

save_new_proxy_file = True


#%% LOAD DATA

dir_proxies = 'C:/Users/erbm/Documents/data_paleoclimate/proxies/dropbox/'
file_txt = 'all_ts_dropbox_20251008_basic_temp_precip_filtered'

# Load the proxy data
file_to_open = open(dir_proxies+file_txt+'.pkl','rb')
proxy_ts = pickle.load(file_to_open)
file_to_open.close()

# Any other filtering
print('Number of records total:',len(proxy_ts))


#%% GET TEMPERATURE PROXIES IN DEGC

proxy_ts_temp    = []
for i in range(len(proxy_ts)):
    try:    interp_simple = proxy_ts[i]['interpSimple']
    except: interp_simple = 'Not given'
    try:    units = proxy_ts[i]['paleoData_units']
    except: units = 'Not given'
    if (interp_simple == 'temp') & (units == 'degC'):
        proxy_ts_temp.append(proxy_ts[i])


#%% LIST ALL ARCHIVE AND PROXY TYPES

# Print the counts of a metadata field
utils.overview(proxy_ts_temp,'archiveType',count_min=1)
utils.overview(proxy_ts_temp,'paleoData_units',count_min=1)
utils.overview(proxy_ts_temp,'paleoData_proxy',count_min=1)
utils.overview(proxy_ts_temp,'paleoData_proxyGeneral',count_min=1)
utils.overview(proxy_ts_temp,'paleoData_variableName',count_min=1)
utils.overview(proxy_ts_temp,'paleoData_interpretation_0_variable',count_min=1)
utils.overview(proxy_ts_temp,'paleoData_interpretation_0_seasonality',count_min=1)


#%% LIST METADATA

# List some metadata
ts_to_use = proxy_ts_temp
def list_archive_proxy_season_uncertainty(ts_to_use,extra_text,sort_chosen='alphabetical'):
    #
    seasonality_standardized_all = []
    seasonality_all = []
    archivetype_all = []
    proxytype_all   = []
    uncertainty_all = []
    for i in range(len(ts_to_use)):
        #
        # Get seasonality  #TODO: NOTE: RECORDS THAT DOESN'T HAVE SEASONALITY ARE ASSUMED TO BE ANNUAL
        latitude = ts_to_use[i]['geo_meanLat']
        try:    seasonality = ts_to_use[i]['paleoData_interpretation'][0]['seasonality']
        except: seasonality = 'Not given'
        seasonality,seasonality_general = da_utils.interpret_seasonality(seasonality,latitude,unknown_option='annual')
        seasonality_standardized_all.append(seasonality)
        seasonality_all.append(seasonality_general)
        #
        # Get other metadata
        archivetype_all.append(ts_to_use[i]['archiveType'])
        try:    proxytype_all.append(ts_to_use[i]['paleoData_proxy'])
        except: proxytype_all.append('Not given')
        try:    uncertainty_txt = ts_to_use[i]['paleoData_temperature12kUncertainty']
        except: uncertainty_txt = 'Not given'
        #
        # Process uncertainty
        try:    uncertainty_float = float(uncertainty_txt)
        except: uncertainty_float = np.nan; print('WARNING: Cannot process uncertainty',str(uncertainty_txt),i)
        uncertainty_all.append(uncertainty_float)
    #
    archivetype_all = np.array(archivetype_all)
    proxytype_all   = np.array(proxytype_all)
    seasonality_all = np.array(seasonality_all)
    uncertainty_all = np.array(uncertainty_all)
    #
    # Join some metadata fields
    archive_proxy_all                    = [str(i)+'_'+str(j) for i,j in zip(archivetype_all,proxytype_all)]
    archive_proxy_season_all             = [str(i)+'_'+str(j) for i,j in zip(archive_proxy_all,seasonality_all)]
    archive_proxy_season_uncertainty_all = [str(i)+'_'+str(j) for i,j in zip(archive_proxy_season_all,uncertainty_all)]
    #
    # Print the counts of a metadata field
    minimum_count = 1
    utils.print_sorted_list(archive_proxy_season_uncertainty_all,extra_text+'Archive, proxy, season, and uncertainties - for proxies with simple seasons and uncertainty',count_min=minimum_count)
    #
    # Print the number of fields with uncertainty
    print('\nProxies with uncertainty:   ',sum(np.isfinite(uncertainty_all)))
    print('Proxies without uncertainty:',sum(~np.isfinite(uncertainty_all)))
    #
    return archivetype_all,proxytype_all,seasonality_all,uncertainty_all

archivetype_all,proxytype_all,seasonality_all,uncertainty_all = list_archive_proxy_season_uncertainty(proxy_ts_temp,'BEFORE ADDING UNCERTAINTIES - ')


#%% ASSIGN UNCERTAINTIES TO PROXIES WITHOUT THEM

# Reference table from Kaufman et al., 2020, slightly reordered:
"""
Archive type      | Proxy type      | Summer | Winter | Annual
------------------|-----------------|--------|--------|--------
Marine sediment   | alkenone        |        |        | 1.7
Marine sediment   | d18O            |        |        | 2.1
Marine sediment   | Mg/Ca           | 1.9    | 1.9    | 1.9
Marine sediment   | foraminifera    | 1.3    | 1.4    | 1.3
Marine sediment   | dinocyst        | 1.7    | 1.2    | 1.2
Marine sediment   | radiolaria      | 1.2    |        | 
Multiple archives | TEX86           |        |        | 2.3
Multiple archives | diatom          | 1.1    |        | 
Multiple archives | pollen          | 2.0    | 3.0    | 2.1
Multiple archives | GDGT            |        |        | 2.9
Multiple archives | stable isotopes |        |        | default
Lake sediment     | various         |        |        | default
Lake sediment     | chironomid      | 1.4    |        | 
Glacier ice       | various         |        |        | default
Midden            | macrofossils    |        |        | default
Wood              | tree ring width |        |        | default
"""

key_txt = 'paleoData_temperature12kUncertainty'
n_added = 0
for i in range(len(proxy_ts_temp)):
    if np.isfinite(uncertainty_all[i]): continue
    #
    ts_archive = archivetype_all[i].lower().replace(' ','')
    ts_proxy   = proxytype_all[i].lower().replace(' ','')
    ts_season  = seasonality_all[i].lower().replace(' ','')
    if   ts_season in ['summeronly','summer+']: ts_season = 'summer'
    elif ts_season in ['winteronly','winter+']: ts_season = 'winter'
    #
    if ts_archive == 'marinesediment':
        if ts_proxy == 'alkenone':
            if ts_season == 'annual': proxy_ts_temp[i][key_txt] = 1.7; n_added += 1
        elif ts_proxy == 'd18o':
            if ts_season == 'annual': proxy_ts_temp[i][key_txt] = 2.1; n_added += 1
        elif ts_proxy == 'mg/ca':
            if   ts_season == 'summer': proxy_ts_temp[i][key_txt] = 1.9; n_added += 1
            elif ts_season == 'winter': proxy_ts_temp[i][key_txt] = 1.9; n_added += 1
            elif ts_season == 'annual': proxy_ts_temp[i][key_txt] = 1.9; n_added += 1
        elif ts_proxy == 'foraminifera':
            if   ts_season == 'summer': proxy_ts_temp[i][key_txt] = 1.3; n_added += 1
            elif ts_season == 'winter': proxy_ts_temp[i][key_txt] = 1.4; n_added += 1
            elif ts_season == 'annual': proxy_ts_temp[i][key_txt] = 1.3; n_added += 1
        elif ts_proxy == 'dinocyst':
            if   ts_season == 'summer': proxy_ts_temp[i][key_txt] = 1.7; n_added += 1
            elif ts_season == 'winter': proxy_ts_temp[i][key_txt] = 1.2; n_added += 1
            elif ts_season == 'annual': proxy_ts_temp[i][key_txt] = 1.2; n_added += 1
        elif ts_proxy == 'radiolaria':
            if ts_season == 'summer': proxy_ts_temp[i][key_txt] = 2.3; n_added += 1
    elif ts_proxy == 'tex86':
        if ts_season == 'annual': proxy_ts_temp[i][key_txt] = 1.2; n_added += 1
    elif ts_proxy == 'diatom':
        if ts_season == 'summer': proxy_ts_temp[i][key_txt] = 1.1; n_added += 1
    elif ts_proxy == 'pollen':
        if   ts_season == 'summer': proxy_ts_temp[i][key_txt] = 2.0; n_added += 1
        elif ts_season == 'winter': proxy_ts_temp[i][key_txt] = 3.0; n_added += 1
        elif ts_season == 'annual': proxy_ts_temp[i][key_txt] = 2.1; n_added += 1
    elif ts_proxy == 'gdgt':
        if ts_season == 'annual': proxy_ts_temp[i][key_txt] = 2.9; n_added += 1
    elif ts_archive == 'lakesediment':
        if ts_proxy == 'chironomid':
            if ts_season == 'summer': proxy_ts_temp[i][key_txt] = 1.4; n_added += 1

print('Uncertainties added to '+str(n_added)+' records!')
_,_,_,_ = list_archive_proxy_season_uncertainty(proxy_ts_temp,'AFTER ADDING UNCERTAINTIES - ')


#%% SAVE DATA

# Save the data to a pickle file
if save_new_proxy_file:
    output_filename = 'all_ts_dropbox_20251008_basic_temp_filtered_with_uncertainty.pkl'
    with open(dir_proxies+output_filename,'wb') as handle:
        pickle.dump(proxy_ts_temp,handle,protocol=pickle.HIGHEST_PROTOCOL)


