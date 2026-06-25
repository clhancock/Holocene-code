#==============================================================================
# This script contains the main code of the Holocene data assimilation.
# Options are set in the config yml file. See README.txt for a more complete
# explanation of the code and setup.
# ---
# This version of the code has been updated to focus on North America for the
# North American ecological sensitivity project.
# ---
#    author: Michael Erb
#==============================================================================

# Change working directory
import os
os.chdir('C:/Users/erbm/Documents/GitHub/Holocene-code/')

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import yaml
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import da_load_models

save_instead_of_plot = False


#%% SETTINGS

# Use a given config file
config_file = 'config.yml'
seed_overwrite = 'None'

# Load the configuration options and print them to the screen.
print('Using configuration file: '+config_file)
with open(config_file,'r') as file: options = yaml.load(file,Loader=yaml.FullLoader)

# Get the root vars
vars_to_reconstruct = options['vars_to_reconstruct']
vars_to_reconstruct_root = [var.split('_')[0] for var in vars_to_reconstruct]
options['vars_root'] = np.unique(vars_to_reconstruct_root)

print('=== SETTINGS ===')
for key in options.keys():
    print('%30s: %-15s' % (key,str(options[key])))
print('=== END SETTINGS ===')



#%% LOAD AND PROCESS MODEL DATA

# Load the chosen model data
model_data = da_load_models.load_model_data(options)
n_models_in_prior = len(options['models_for_prior'])

# If the prior is allowed to change through time, remove the mean of the reference period from each model.
if options['reconstruction_type'] == 'relative':
    print('Processing model: relative reconstruction')
    for i in range(n_models_in_prior):
        ind_for_model = (model_data['number'] == (i+1))
        ind_ref = (model_data['age'] >= options['reference_period'][0]) & (model_data['age'] < options['reference_period'][1]) & ind_for_model
        for var in options['vars_root']:
            model_data[var][ind_for_model,:,:,:] = model_data[var][ind_for_model,:,:,:] - np.mean(model_data[var][ind_ref,:,:,:],axis=0)
        for var in options['vars_to_reconstruct']:
            model_data[var][ind_for_model,:,:]   = model_data[var][ind_for_model,:,:]   - np.mean(model_data[var][ind_ref,:,:],axis=0)


#%% PLOT COVARIANCE PATTERNS ON A GRID

# Get model data
model_tas_annual = model_data['tas_annual']
model_lat = model_data['lat']
model_lon = model_data['lon']
model_age = model_data['age']

# Get data for the last 5100 years
ind_selected = np.where((model_age > 0) & (model_age <= 5100))[0]
model_tas_annual = model_tas_annual[ind_selected,:,:]
model_age = model_age[ind_selected]
#model_tas_annual_mean = np.mean(model_tas_annual,axis=0)

# Set locations for covariance testing
lats_to_test = np.arange(20,70,20)
lons_to_test = np.arange(-120,-50,20) + 360
lats_to_test_all,lons_to_test_all = np.meshgrid(lats_to_test,lons_to_test)
lats_to_test_all = lats_to_test_all.flatten()
lons_to_test_all = lons_to_test_all.flatten()

# Set things up
n_locs = len(lats_to_test_all)
n_lat = len(model_lat)
n_lon = len(model_lon)
covariances_all = np.zeros((n_locs,n_lat,n_lon)); covariances_all[:] = np.nan
correlations_all = np.zeros((n_locs,n_lat,n_lon)); correlations_all[:] = np.nan
locs_all = np.zeros((n_locs,2)); locs_all[:] = np.nan

# Compute all covariance patterns
k=0
for k in range(n_locs):
    #
    print(k)
    #
    lat_selected = lats_to_test_all[k]
    lon_selected = lons_to_test_all[k]
    #
    # Get values near the selected location.
    j_selected = np.argmin(np.abs(lat_selected - model_lat))
    i_selected = np.argmin(np.abs(lon_selected - model_lon))
    locs_all[k,:] = model_lon[i_selected],model_lat[j_selected]
    #
    # Get model values and compute covariances
    model_values_selected = model_tas_annual[:,j_selected,i_selected]
    for j in range(n_lat):
        for i in range(n_lon):
            correlations_all[k,j,i] = np.corrcoef(model_values_selected,model_tas_annual[:,j,i])[0,1]
            #correlations_all[k,j,i] = np.cov(model_values_selected,model_tas_annual[:,j,i])[0,1]


#%% FIGURES - MAPS

k=2

def map_correlations(k):
    
    # Make a map
    plt.figure(figsize=(10,12))
    region_to_plot = [-160,-40,0,80]
    region_center = (region_to_plot[0]+region_to_plot[1])/2
    ax1 = plt.subplot2grid((1,1),(0,0),projection=ccrs.LambertConformal(central_longitude=region_center)); ax1.set_extent(region_to_plot,ccrs.PlateCarree())
    
    map1 = ax1.contourf(model_lon,model_lat,correlations_all[k,:,:],np.arange(-1,1.1,.1),extend='both',cmap='bwr',transform=ccrs.PlateCarree())  # 
    ax1.scatter(locs_all[k,0],locs_all[k,1],100,c='yellow',marker='o',edgecolor='k',alpha=1,transform=ccrs.PlateCarree())
    colorbar1 = plt.colorbar(map1,orientation='horizontal',ax=ax1,fraction=0.08,pad=0.02)
    colorbar1.ax.tick_params(labelsize=14)
    colorbar1.ax.set_facecolor('none')
    #ax1.set_title(title_txt+' - Mean temperature for '+str(age_bounds[0]/1000)+'-'+str(age_bounds[1]/1000)+'ka vs 3-5ka\n'+exp_txt,loc='center',fontsize=18)
    ax1.coastlines()
    ax1.add_feature(cfeature.LAKES,facecolor='none',edgecolor='k')
    ax1.gridlines(color='k',linewidth=1,linestyle=(0,(1,5)))
    ax1.spines['geo'].set_edgecolor('black')
    
    if save_instead_of_plot:
        #plt.savefig('figures/script1_2_map_'+exp_txt+'_'+title_txt+'_'+str(file_num+1).zfill(2)+'_ages_'+str(age_bounds[0])+'_'+str(age_bounds[1])+'_yr_BP.png',dpi=300,format='png',bbox_inches='tight')
        plt.close()
    else:
        plt.show()

for k in range(n_locs):
    map_correlations(k)

