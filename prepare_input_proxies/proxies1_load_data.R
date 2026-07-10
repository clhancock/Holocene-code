#===============================================================================
# This package loads the proxy database and stores it in an easier-to-load format.
#  - https://nickmckay.org/lipdR/
#  - https://nickmckay.org/GeoChronR/articles/TsFilteringAndMapping.html
# author: Michael Erb
#===============================================================================

library(lipdR)
library(geoChronR)

data_dir <- 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'

# LOAD PROXIES =================================================================

proxies_all <- readLipd(paste0(data_dir,'database/'))
all_ts <- extractTs(proxies_all)

# SAVE DATA ====================================================================

# Save data into a different format
date_today <- as.character(Sys.Date())
saveRDS(proxies_all, file=paste0(data_dir,'proxy_ts_',date_today,'.rds'))
