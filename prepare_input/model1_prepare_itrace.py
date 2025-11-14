#==============================================================================
# Make some plots using the new iTRACE Holocene simulation.
#    author: Michael Erb
#    date  : 10/27/2025
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import netCDF4

plt.style.use('ggplot')
save_instead_of_plot = False


#%% LOAD DATA

output_dir = 'C:/Users/erbm/Dropbox/Academia/NAU/Project_EcoClimate_Sensitivity/analysis/3_explore_models/figures/'

# Load the iTRACE data
time_resolution = 10
data_dir_itrace = 'C:/Users/erbm/Documents/data_paleoclimate/models/itrace/'
handle_itrace = xr.open_dataset(data_dir_itrace+'b.e13.Bi1850C5.f19_g16.all.21_12ka.itrace.ice_ghg_orb_wtr.cam.h0.TREFHT.000101-899912.res_'+str(time_resolution)+'.nc')
trefht_itrace = handle_itrace['TREFHT'].values
lat_itrace    = handle_itrace['lat'].values
lon_itrace    = handle_itrace['lon'].values
time_itrace   = handle_itrace['time'].values
handle_itrace.close()
age_itrace = 20000 - time_itrace

# Load the iTRACE data for the Holocene
data_dir_holocene = 'C:/Users/erbm/Documents/data_paleoclimate/models/itrace_holocene/atm-surface/'
handle_holocene = xr.open_dataset(data_dir_holocene+'itrace.11Ka-0Ka.atm.TREFHT.nc',decode_times=False)
trefht_holocene_ann = handle_holocene['TREFHT_ANN'].values
trefht_holocene_mam = handle_holocene['TREFHT_MAM'].values
trefht_holocene_jja = handle_holocene['TREFHT_JJA'].values
trefht_holocene_son = handle_holocene['TREFHT_SON'].values
trefht_holocene_djf = handle_holocene['TREFHT_DJF'].values
lat_holocene        = handle_holocene['lat'].values
lon_holocene        = handle_holocene['lon'].values
age_holocene        = handle_holocene['time'].values
handle_holocene.close()

# Compare lats and lons
print('iTRACE:          ',min(lat_itrace),max(lat_itrace),min(lon_itrace),max(lon_itrace))
print('iTRACE-Holocene: ',min(lat_holocene),max(lat_holocene),min(lon_holocene),max(lon_holocene))
print(lat_itrace - lat_holocene)
print(lon_itrace - lon_holocene)

# Convert units from K to C
trefht_itrace       = trefht_itrace       - 273.15
trefht_holocene_ann = trefht_holocene_ann - 273.15


#%% CREATE A SORT-OF MONTHLY FILE UNTIL I CAN GET A REAL ONE





#%% COMBINE THE TWO PARTS

# Compute annual means for iTRACE
ndays_per_month = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
trefht_itrace_ann = np.average(trefht_itrace,axis=1,weights=ndays_per_month)

# Combine the older and newer segments
trefht_combined = np.concatenate((trefht_itrace_ann,trefht_holocene_ann),axis=0)
age_combined = np.concatenate((age_itrace,age_holocene),axis=0)
lat_combined = lat_itrace
lon_combined = lon_itrace


#%% TRIM TO ONLY THE NORTH AMERICAN REGION

# Set bounds of interest
lat_bounds = [10,80]
lon_bounds = [360-173,360-48]  # 173-48W

# Trim data
j_selected = np.where((lat_combined >= lat_bounds[0]) & (lat_combined <= lat_bounds[1]))[0]
i_selected = np.where((lon_combined >= lon_bounds[0]) & (lon_combined <= lon_bounds[1]))[0]
trefht_combined_trimmed = trefht_combined[:,j_selected,:][:,:,i_selected]
lat_trimmed = lat_combined[j_selected]
lon_trimmed = lon_combined[i_selected]


#%% AVERAGE FROM DECADAL TO 200 YEAR

n_decades = trefht_combined_trimmed.shape[0]
n_lat     = trefht_combined_trimmed.shape[1]
n_lon     = trefht_combined_trimmed.shape[2]

trefht_200yr = np.nanmean(np.reshape(trefht_combined_trimmed,(int(n_decades/20),20,n_lat,n_lon)),axis=1)
age_200yr    = np.nanmean(np.reshape(age_combined,           (int(n_decades/20),20)),            axis=1)


#%% SAVE MODEL OUTPUT

output_dir = 'C:/Users/erbm/Documents/data_assimilation/models/processed_model_data/'

# Save model output
outputfile = netCDF4.Dataset(output_dir+'itrace.19999-0BP.tas.timeres_10.nc','w')
outputfile.createDimension('age',  age_combined.shape[0])
outputfile.createDimension('month',12)
outputfile.createDimension('lat',  len(lat_trimmed))
outputfile.createDimension('lon',  len(lon_trimmed))

output_var       = outputfile.createVariable('tas','f8',('age','month','lat','lon',))
output_age       = outputfile.createVariable('age','f8',('age',))
output_lat       = outputfile.createVariable('lat','f8',('lat',))
output_lon       = outputfile.createVariable('lon','f8',('lon',))
output_ndays     = outputfile.createVariable('days_per_month','f8',('month',))
output_ndays_all = outputfile.createVariable('days_per_month_all','f8',('age','month',))

output_var[:]       = trefht_combined_trimmed
output_age[:]       = age_combined
output_lat[:]       = lat_trimmed
output_lon[:]       = lon_trimmed
output_ndays[:]     = time_ndays_model
output_ndays_all[:] = time_ndays_model_nyearmean

outputfile.close()

