#==============================================================================
# Make some plots using the new iTRACE Holocene simulation.
#    author: Michael Erb
#    date  : 10/15/2025
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

output_dir = 'C:/Users/erbm/Dropbox/Academia/NAU/Manuscripts/Project_EcoClimate_Sensitivity/analysis/3_explore_models/figures/'

# Load the iTRACE data
data_dir_itrace   = 'C:/Users/erbm/Documents/data_assimilation/results/'
handle_itrace = xr.open_dataset(data_dir_itrace+'b.e13.Bi1850C5.f19_g16.all.21_12ka.itrace.ice_ghg_orb_wtr.cam.h0.TREFHT.000101-899912.res_'+str(time_resolution)+'.nc')
trefht_itrace = handle_itrace['TREFHT'].values
lat_itrace    = handle_itrace['lat'].values
lon_itrace    = handle_itrace['lon'].values
time_itrace   = handle_itrace['time'].values
handle_itrace.close()
age_itrace = 20000 - time_itrace


# Compare lats and lons
print('iTRACE:          ',min(lat_itrace),max(lat_itrace),min(lon_itrace),max(lon_itrace))
print('iTRACE-Holocene: ',min(lat_holocene),max(lat_holocene),min(lon_holocene),max(lon_holocene))
print(lat_itrace - lat_holocene)
print(lon_itrace - lon_holocene)

# Convert units from K to C
trefht_itrace       = trefht_itrace       - 273.15
trefht_holocene_ann = trefht_holocene_ann - 273.15


#%% CALCULATIONS

# Compute annual means for iTRACE
ndays_per_month = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
trefht_itrace_ann = np.average(trefht_itrace,axis=1,weights=ndays_per_month)

# This function takes a time-lat-lon variable and computes the mean for a given range of lon and lat.
def spatial_mean(variable,lat_model,lon_model,lat_min,lat_max,lon_min,lon_max):
    #
    j_selected = np.where((lat_model >= lat_min) & (lat_model <= lat_max))[0]
    i_selected = np.where((lon_model >= lon_min) & (lon_model <= lon_max))[0]
    print('Computing spatial mean. lats='+str(lat_model[j_selected[0]])+'-'+str(lat_model[j_selected[-1]])+', lons='+str(lon_model[i_selected[0]])+'-'+str(lon_model[i_selected[-1]])+'.  Points are inclusive.')
    #
    lat_weights = np.cos(np.radians(lat_model))
    variable_zonal = np.nanmean(variable[:,:,i_selected],axis=2)
    variable_mean = np.average(variable_zonal[:,j_selected],axis=1,weights=lat_weights[j_selected])
    #
    return variable_mean

# Compute Arctic means
na_itrace   = spatial_mean(trefht_itrace_ann,  lat_itrace,  lon_itrace,  10,75,360-170,360-45)
na_holocene = spatial_mean(trefht_holocene_ann,lat_holocene,lon_holocene,10,75,360-170,360-45)
gmt_itrace   = spatial_mean(trefht_itrace_ann,  lat_itrace,  lon_itrace,  -90,90,0,360)
gmt_holocene = spatial_mean(trefht_holocene_ann,lat_holocene,lon_holocene,-90,90,0,360)


#%% FIGURES

# Plot time series
#f,ax1 = plt.subplots(2,1,figsize=(12,6))
f = plt.figure(figsize=(16,10))
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0))

ax1.plot(age_itrace,gmt_itrace,c='k',label='iTRACE')
ax1.plot(age_holocene,gmt_holocene,c='tab:blue',label='iTRACE-Holocene')
ax1.set_title('Temperature for global-mean ($^\circ$C)',fontsize=18)
ax1.legend()
ax1.set_xlim(20000,0)
#ax1.set_xlabel('Age (yr B.P.)',fontsize=16)
ax1.set_ylabel('T ($^\circ$C)',fontsize=16)

ax2.plot(age_itrace,na_itrace,c='k',label='iTRACE')
ax2.plot(age_holocene,na_holocene,c='tab:blue',label='iTRACE-Holocene')
ax2.set_title('Temperature for North American region ($^\circ$C)',fontsize=18)
ax2.legend()
ax2.set_xlim(20000,0)
ax2.set_xlabel('Age (yr B.P.)',fontsize=16)
ax2.set_ylabel('T ($^\circ$C)',fontsize=16)

if save_instead_of_plot:
    plt.savefig(output_dir+'models_arctic_temp_ts_itrace_holocene.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()
