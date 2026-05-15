#==============================================================================
# Load proxies, process them, and save the selected proxies.
#    author: Michael Erb
#==============================================================================

#import lipd
from pylipd.lipd import LiPD

#%% LOAD DATA

# Load the proxy data
dir_proxies = 'C:/Users/erbm/Documents/GitHub/Holocene-code/prepare_input/process_proxies_compare/example_for_nick/'
proxies_all = lipd.readLipd(dir_proxies+'3cBx.Sagawa.2012.lpd')
all_ts = lipd.extractTs(proxies_all)
print('N proxies: ',len(proxies_all))
print('N timeseries: ',len(all_ts))
