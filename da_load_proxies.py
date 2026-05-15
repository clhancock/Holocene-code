#==============================================================================
# Functions for loading proxy data for the data assimilation project.
#    author: Michael P. Erb
#==============================================================================

import da_utils
import numpy as np
import lipd
from scipy import interpolate
import rdata

# A function to load the chosen proxy datasets
def load_proxies(options):
    #
    # Create lists to the store the proxy data in
    collection_all = []
    proxy_ts       = []
    #
    n_datasets = len(options['proxy_datasets_to_assimilate'])
    #i = 0; proxy_dataset = options['proxy_datasets_to_assimilate'][i]
    for i,proxy_dataset in enumerate(options['proxy_datasets_to_assimilate']):
        print('Loading proxy dataset '+str(i+1)+'/'+str(n_datasets)+': '+proxy_dataset)
        proxy_dataset_short = proxy_dataset.split('_')[0]
        if proxy_dataset_short == 'ecoclimate':
            #
            # Load the EcoClimate proxy metadata
            proxy_ts_ecoclimate = rdata.read_rds(options['data_dir']+'proxies/ecoclimate/'+proxy_dataset+'.rds')
            if options['reconstruction_type'] == 'absolute': proxy_ts_ecoclimate = lipd.filterTs(proxy_ts_ecoclimate,'paleoData_datum == abs')
            #
            # Add these proxies to the full proxy dataset
            proxy_ts = proxy_ts + proxy_ts_ecoclimate
            collection_all = collection_all + ([proxy_dataset_short] * len(proxy_ts_ecoclimate))
            #
        else:
            print('ERROR: invalid proxy dataset: '+proxy_dataset)
    #
    return proxy_ts,collection_all


# Filter the proxy data
def filter_proxies_and_set_psms(proxy_ts,collection_all,options):
    #
    # Set up variables
    print('Filtering proxies and assigning PSMs')
    n_proxies = len(proxy_ts)
    print('Proxies, all loaded:',n_proxies)
    logical_selected_all = np.array([False]*n_proxies)
    proxy_psms = ["None"]*n_proxies
    #
    # Get some metadata fields from proxies
    proxy_archivetype = []
    proxy_interp      = []
    proxy_units       = []
    for i in range(n_proxies):
        try:    proxy_archivetype.append(proxy_ts[i]['archiveType'][0])
        except: proxy_archivetype.append("Not given")
        try:    proxy_interp.append(proxy_ts[i]['interpretation1_variable'][0])
        except: proxy_interp.append("Not given")
        try:    proxy_units.append(proxy_ts[i]['paleoData_units'][0])
        except: proxy_units.append("Not given")
    #
    # Find the proxies to keep
    n_combinations = len(options['proxies_to_use'])
    for i in range(n_combinations):
        #
        combination_selected = options['proxies_to_use'][0]
        chosen_archivetype = combination_selected.split('|')[0]
        chosen_interp      = combination_selected.split('|')[1]
        chosen_unit        = combination_selected.split('|')[2]
        chosen_psm         = combination_selected.split('|')[3]
        logical_archivetype = np.array(proxy_archivetype) == chosen_archivetype
        logical_interp      = np.array(proxy_interp)      == chosen_interp
        logical_unit        = np.array(proxy_units)       == chosen_unit
        if chosen_archivetype == 'any': logical_archivetype[:] = True
        if chosen_interp      == 'any': logical_interp[:]      = True
        if chosen_unit        == 'any': logical_unit[:]        = True
        logical_selected = logical_archivetype & logical_interp & logical_unit
        ind_selected = np.where(logical_selected)[0]
        print('Proxies in group ('+combination_selected+'):',len(ind_selected))
        #
        # Set the PSM
        for index in ind_selected:
            proxy_psms[index] = chosen_psm
        #
        # Combine each logical combination
        logical_selected_all = logical_selected_all | logical_selected
    #
    ind_selected_all = np.where(logical_selected_all)[0]
    print('Proxies in all groups:',len(ind_selected_all))
    #
    # Get proxy data to keep
    proxy_ts_selected   = [proxy_ts[index]       for index in ind_selected_all]
    psms_selected       = [proxy_psms[index]     for index in ind_selected_all]
    collection_selected = [collection_all[index] for index in ind_selected_all]
    #
    return proxy_ts_selected,psms_selected,collection_selected


# Process the proxy data
#def process_proxies(proxy_ts,collection_all,options):
def process_proxies(proxy_ts_selected,psms_selected,collection_selected,options):
    #
    print('\n=== Processing proxy data. This can take a few minutes. Please wait. ===')
    #
    # Set age range to reconstruct, as well as the reference period (The -0.5 accounts for the fact that age years are represented as whole numbers)
    age_bounds = np.arange(options['age_range_to_reconstruct'][0],options['age_range_to_reconstruct'][1]+1,options['time_resolution']) - 0.5
    age_centers = (age_bounds[:-1]+age_bounds[1:])/2
    #
    # Set the maximum proxy resolution
    max_res_value = int(options['maximum_resolution']/options['time_resolution'])
    #
    # Get dimensions
    n_ages    = len(age_centers)
    n_proxies = len(proxy_ts_selected)
    #
    # Set up arrays for the processed proxy data to be stored in
    proxy_data = {}
    proxy_data['values_binned']     = np.zeros((n_proxies,n_ages));          proxy_data['values_binned'][:]     = np.nan
    proxy_data['resolution_binned'] = np.zeros((n_proxies,n_ages));          proxy_data['resolution_binned'][:] = np.nan
    proxy_data['metadata']          = np.zeros((n_proxies,11),dtype=object); proxy_data['metadata'][:]          = np.nan
    proxy_data['lats']              = np.zeros((n_proxies));                 proxy_data['lats'][:]              = np.nan
    proxy_data['lons']              = np.zeros((n_proxies));                 proxy_data['lons'][:]              = np.nan
    #proxy_data['uncertainty']       = np.zeros((n_proxies));                 proxy_data['uncertainty'][:]       = np.nan
    proxy_data['uncertainty']       = []
    proxy_data['archivetype']       = []
    proxy_data['proxytype']         = []
    proxy_data['units']             = []
    proxy_data['interp']            = []
    proxy_data['direction']         = []
    proxy_data['seasonality_array'] = {}
    proxy_data['psm']               = []
    #
    # Loop through proxies, saving the necessary values to common variables.
    no_ref_data = 0; missing_uncertainty = 0
    i = 0
    for i in range(n_proxies):
        #
        # Get proxy data
        print('Processing proxies:',i)
        proxy_values = np.array(proxy_ts_selected[i]['paleoData_values']).astype(float)
        keys = list(proxy_ts_selected[i].keys())
        if 'age' in keys:
            proxy_ages = np.array(proxy_ts_selected[i]['age']).astype(float)
        elif 'year' in keys:
            proxy_years = np.array(proxy_ts_selected[i]['year']).astype(float)
            proxy_ages = 1950 - proxy_years  # TODO: Check this.
        else:
            print(' === WARNING: No ages or years in index',i,' SKIPPING ===')
            continue
        #
        # If any NaNs exist in the ages, remove those values
        proxy_values = proxy_values[np.isfinite(proxy_ages)]
        proxy_ages   = proxy_ages[np.isfinite(proxy_ages)]
        #
        # Sort the data so that ages go from newest to oldest
        ind_sorted = np.argsort(proxy_ages)
        proxy_values = proxy_values[ind_sorted]
        proxy_ages   = proxy_ages[ind_sorted]
        #
        # Update the units:
        #TODO: Work on this, and update uncertainty as well
        #  - Precipitation: mm/yr -> mm/day
        try:    data_units = proxy_ts_selected[i]['paleoData_units'][0]
        except: data_units = 'Not given'
        if data_units == 'mm/yr':
            proxy_values = proxy_values/365.25  #TODO: Consider using a different value than 365.25
            data_units = 'mm/day'
            print('Proxy '+str(i)+': Updating units from mm/yr to mm/day')
        #
        # INTERPOLATION
        # To interpolate the proxy data to the base resolution (by default: decadal):
        #   1. Values in the same year are averaged
        #   2. Records are then interpolated to annual using nearest neighbor interpolation
        #   3. Records are binned to the base resolution
        # To get the mean resolution of the proxy data at each time interval, it is treated in a similar way.
        #
        # Average values in the same year
        if min(proxy_ages[1:]-proxy_ages[:-1]) < 1:
            proxy_values_ann = []
            proxy_ages_ann   = []
            for int_age in np.arange(int(np.floor(proxy_ages[0])),int(np.ceil(proxy_ages[-1])+1)):
                ind_in_year = np.where((proxy_ages > int_age) & (proxy_ages <= (int_age+1)))[0]
                if len(ind_in_year) > 0:
                    proxy_values_ann.append(np.nanmean(proxy_values[ind_in_year]))
                    proxy_ages_ann.append(np.nanmean(proxy_ages[ind_in_year]))
            #
            proxy_values_ann = np.array(proxy_values_ann)
            proxy_ages_ann   = np.array(proxy_ages_ann)
        else:
            proxy_values_ann = proxy_values
            proxy_ages_ann   = proxy_ages
        #
        # Represent annual proxy ages as integers, where e.g., age 100 represent values <=100 and >99
        proxy_ages = np.ceil(proxy_ages)
        #
        # Compute age bounds of the proxy observations as the midpoints between data
        proxy_age_bounds = (proxy_ages_ann[1:]+proxy_ages_ann[:-1])/2
        end_newest = proxy_ages_ann[0]  - (proxy_ages_ann[1]-proxy_ages_ann[0])/2
        end_oldest = proxy_ages_ann[-1] + (proxy_ages_ann[-1]-proxy_ages_ann[-2])/2
        proxy_age_bounds = np.insert(proxy_age_bounds,0,end_newest)
        proxy_age_bounds = np.append(proxy_age_bounds,end_oldest)
        proxy_res_ann = proxy_age_bounds[1:] - proxy_age_bounds[:-1]
        #
        """
        # Checking calculations
        import matplotlib.pyplot as plt
        plt.plot(proxy_ages,proxy_values,'ko')
        plt.plot(proxy_ages_ann,proxy_values_ann,'b-')
        plt.show()
        """
        #
        # Use nearest neighbor interpolation to get data to the interpolation resolution
        interp_res = 1
        interp_function = interpolate.interp1d(proxy_ages_ann,proxy_values_ann,kind='nearest',bounds_error=False,fill_value='extrapolate')
        proxy_ages_interp = np.arange(int(np.ceil(end_newest)),int(np.floor(end_oldest))+interp_res,interp_res)
        proxy_values_interp = interp_function(proxy_ages_interp)
        #
        # Use nearest neighbor interpolation to get the resolution to annual
        interp_function_res = interpolate.interp1d(proxy_ages_ann,proxy_res_ann,kind='nearest',bounds_error=False,fill_value='extrapolate')
        proxy_res_interp = interp_function_res(proxy_ages_interp)
        #
        # Bin the annual data to the base resolution
        proxy_values_12ka = np.zeros((n_ages)); proxy_values_12ka[:] = np.nan
        proxy_res_12ka    = np.zeros((n_ages)); proxy_res_12ka[:]    = np.nan
        for j in range(n_ages):
            ind_selected = np.where((proxy_ages_interp >= age_bounds[j]) & (proxy_ages_interp < age_bounds[j+1]))[0]
            proxy_values_12ka[j] = np.nanmean(proxy_values_interp[ind_selected])
            res_avg              = np.nanmean(proxy_res_interp[ind_selected])
            if np.isnan(res_avg): proxy_res_12ka[j] = np.nan
            else:                 proxy_res_12ka[j] = int(round(res_avg / options['time_resolution']))
        #
        """
        # Checking calculations
        import matplotlib.pyplot as plt
        plt.plot(proxy_ages,proxy_values,'ko')
        plt.plot(proxy_ages_interp,proxy_values_interp,'b-')
        plt.plot(age_centers,proxy_values_12ka,'g-')
        plt.xlim(21000,0)
        plt.show()
        """
        #
        # Get uncertainty metadata  #TODO: Figure out a better uncertainty estimate
        missing_uncertainty_value = np.nan
        #missing_uncertainty_value = 1
        try:    proxy_uncertainty = proxy_ts_selected[i]['paleoData_temperature12kUncertainty'][0]
        except: proxy_uncertainty = missing_uncertainty_value; missing_uncertainty += 1
        if proxy_uncertainty == 'NA': proxy_uncertainty = missing_uncertainty_value; missing_uncertainty += 1
        proxy_uncertainty = np.square(float(proxy_uncertainty))  # Proxy uncertainty was give as RMSE, but the code uses MSE
        #
        # Set resolutions to a minimum of 1 and a maximum of max_res_value
        proxy_res_12ka[proxy_res_12ka < 1] = 1
        proxy_res_12ka[proxy_res_12ka > max_res_value] = max_res_value
        #
        # If the reconstruction type is "relative," remove the mean of the reference period
        if options['reconstruction_type'] == 'relative':
            # The reference period is calculated using annualized data in this case.
            ind_ref = np.where((proxy_ages_interp >= options['reference_period'][0]) & (proxy_ages_interp < options['reference_period'][1]))[0]  
            proxy_values_12ka = proxy_values_12ka - np.nanmean(proxy_values_interp[ind_ref])
            if np.isnan(proxy_values_interp[ind_ref]).all(): print('No data in reference period, index: '+str(i)); no_ref_data += 1
        #
        # Get proxy metdata
        proxy_lat                 = proxy_ts_selected[i]['geo_latitude'][0]
        proxy_lon                 = proxy_ts_selected[i]['geo_longitude'][0]
        try:    proxy_seasonality_txt = proxy_ts_selected[i]['interpretation1_seasonality'][0]
        except: proxy_seasonality_txt = 'Not given'
        try:    proxy_type = proxy_ts_selected[i]['paleoData_proxy'][0]
        except: proxy_type = 'Not given'
        proxy_data['archivetype'].append(proxy_ts_selected[i]['archiveType'][0])
        proxy_data['proxytype'].append(proxy_type)
        proxy_data['units'].append(data_units)
        proxy_data['interp'].append(proxy_ts_selected[i]['interpretation1_variable'][0])
        try:    interp_direction = proxy_ts_selected[i]['interpretation1_direction'][0]
        except: interp_direction = 'Not given'
        proxy_data['direction'].append(interp_direction)
        proxy_data['psm'].append(psms_selected[i])
        #
        # Convert seasonality to a list of months, with negative values corresponding to the previous year.
        proxy_seasonality,proxy_seasonality_general = da_utils.interpret_seasonality(proxy_seasonality_txt,proxy_lat,unknown_option='annual')
        proxy_seasonality_array = np.array(proxy_seasonality.split()).astype(int)
        #
        # If requested, prescribe seasonalities
        if options['assign_seasonality'] == 'annual':
            proxy_seasonality_array = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
        elif options['assign_seasonality'] == 'summer':
            if proxy_lat >= 0: proxy_seasonality_array = np.array([6,7,8])
            else:              proxy_seasonality_array = np.array([-12,1,2])
        elif options['assign_seasonality'] == 'winter':
            if proxy_lat >= 0: proxy_seasonality_array = np.array([-12,1,2])
            else:              proxy_seasonality_array = np.array([6,7,8])
        elif options['assign_seasonality'] == 'jja':
            proxy_seasonality_array = np.array([6,7,8])
        elif options['assign_seasonality'] == 'djf':
            proxy_seasonality_array = np.array([-12,1,2])
        #
        proxy_data['seasonality_array'][i] = proxy_seasonality_array
        #
        # Save to common variables (y and ya)
        proxy_data['values_binned'][i,:]     = proxy_values_12ka
        proxy_data['resolution_binned'][i,:] = proxy_res_12ka
        proxy_data['uncertainty'].append(proxy_uncertainty)
        #
        # Save some more metadata to a common variables
        if proxy_lon < 0: proxy_lon = proxy_lon+360
        proxy_data['metadata'][i,0] = proxy_ts_selected[i]['dataSetName'][0]
        proxy_data['metadata'][i,1] = proxy_ts_selected[i]['paleoData_TSid'][0]
        proxy_data['metadata'][i,2] = str(proxy_lat)
        proxy_data['metadata'][i,3] = str(proxy_lon)
        proxy_data['metadata'][i,4] = str(proxy_seasonality_array)
        proxy_data['metadata'][i,5] = proxy_seasonality_general
        proxy_data['metadata'][i,6] = str(np.median(proxy_ages[1:]-proxy_ages[:-1]))  #TODO: Consider calculating this a different way.
        proxy_data['metadata'][i,7] = collection_selected[i]
        proxy_data['metadata'][i,8] = data_units
        proxy_data['metadata'][i,9] = proxy_ts_selected[i]['interpretation1_variable'][0]
        proxy_data['metadata'][i,10] = interp_direction
        proxy_data['lats'][i] = proxy_lat
        proxy_data['lons'][i] = proxy_lon
        proxy_data['lons'][i] = proxy_lon
    #
    # Convert data types
    proxy_data['archivetype'] = np.array(proxy_data['archivetype'])
    proxy_data['proxytype']   = np.array(proxy_data['proxytype'])
    proxy_data['units']       = np.array(proxy_data['units'])
    proxy_data['uncertainty'] = np.array(proxy_data['uncertainty'])
    #
    # Save the ages for the reconstruction
    proxy_data['age_centers'] = age_centers
    #
    print('\n=== PROXY DATA LOADED ===')
    print('Proxy datasets loaded (n='+str(len(options['proxy_datasets_to_assimilate']))+'):'+str(options['proxy_datasets_to_assimilate']))
    print('Proxies loaded        (n='+str(len(proxy_ts_selected))+')')
    print('---')
    print('Proxies without data in reference period (n='+str(no_ref_data)+')')
    print('Proxies without uncertainty value        (n='+str(missing_uncertainty)+'). Set to '+str(missing_uncertainty_value))
    print('---')
    print('Data stored in dictionary "proxy_data", with keys and dimensions:')
    for key in list(proxy_data.keys()):
        try:    print('%20s %-15s' % (key,str(proxy_data[key].shape)))
        except: print('%20s %-15s' % (key,str(len(proxy_data[key]))))
    print('=========================\n')
    #
    return proxy_data

"""
# Filter the proxy data
def filter_proxies_and_set_psms_old(proxy_data,collection_all,options):
    #
    # Set up variables
    n_proxies = proxy_data['values_binned'].shape[0]
    logical_selected_all = np.array([False]*n_proxies)
    proxy_data['psm'] = ["None"]*n_proxies
    #
    # Find the proxies to keep
    n_combinations = len(options['proxies_to_use'])
    for i in range(n_combinations):
        #
        combination_selected = options['proxies_to_use'][0]
        chosen_archivetype = combination_selected.split('|')[0]
        chosen_interp      = combination_selected.split('|')[1]
        chosen_unit        = combination_selected.split('|')[2]
        chosen_psm         = combination_selected.split('|')[3]
        logical_archivetype = proxy_data['archivetype']      == chosen_archivetype
        logical_interp      = np.array(proxy_data['interp']) == chosen_interp
        logical_unit        = np.array(proxy_data['units'])  == chosen_unit
        if chosen_archivetype == 'any': logical_archivetype[:] = True
        if chosen_interp      == 'any': logical_interp[:]      = True
        if chosen_unit        == 'any': logical_unit[:]        = True
        logical_selected = logical_archivetype & logical_interp & logical_unit
        ind_selected = np.where(logical_selected)[0]
        #
        # Set the PSM
        for index in ind_selected:
            proxy_data['psm'][index] = chosen_psm
        #
        # Combine each logical combination
        logical_selected_all = logical_selected_all | logical_selected
    #
    # Get proxy data to keep
    ind_selected_all = np.where(logical_selected_all)[0]
    proxy_data_to_keep = {}
    proxy_data_to_keep['values_binned']     = proxy_data['values_binned'][logical_selected_all,:]
    proxy_data_to_keep['resolution_binned'] = proxy_data['resolution_binned'][logical_selected_all,:]
    proxy_data_to_keep['metadata']          = proxy_data['metadata'][logical_selected_all,:]
    proxy_data_to_keep['lats']              = proxy_data['lats'][logical_selected_all]
    proxy_data_to_keep['lons']              = proxy_data['lons'][logical_selected_all]
    proxy_data_to_keep['uncertainty']       = proxy_data['uncertainty'][logical_selected_all]
    proxy_data_to_keep['archivetype']       = proxy_data['archivetype'][logical_selected_all]
    proxy_data_to_keep['proxytype']         = proxy_data['proxytype'][logical_selected_all]
    proxy_data_to_keep['units']             = proxy_data['units'][logical_selected_all]
    proxy_data_to_keep['interp']            = [proxy_data['interp'][index] for index in ind_selected_all]
    proxy_data_to_keep['direction']         = [proxy_data['direction'][index] for index in ind_selected_all]
    proxy_data_to_keep['seasonality_array'] = [proxy_data['seasonality_array'][index] for index in ind_selected_all]
    proxy_data_to_keep['age_centers']       = proxy_data['age_centers']
    proxy_data_to_keep['psm']               = [proxy_data['psm'][index] for index in ind_selected_all]
    #
    collection_to_keep = [collection_all[index] for index in ind_selected_all]
    #
    return proxy_data_to_keep,collection_to_keep
"""