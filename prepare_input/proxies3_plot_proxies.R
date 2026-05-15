#===============================================================================
# This package loads the proxy database so it can be explored and filtered.
# Tutorials:
#  - https://nickmckay.org/GeoChronR/articles/PlotTimeseriesStack.html
# author: Michael Erb
#===============================================================================

library(lipdR)
library(geoChronR)
library(ggplot2)
library(tidyverse)
library(rnaturalearth)
library(rnaturalearthdata)

# LOAD PROXIES =================================================================

# Load the proxy data
data_dir <- 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
data_date <- '2026-02-27'
ts_selected <- readRDS(paste0(data_dir,'selected_ts_',data_date,'.RData'))
metadata_selected <- readRDS(paste0(data_dir,'selected_metadata_',data_date,'.RData'))

# Load country borders
country_borders <- ne_countries(scale="medium",returnclass="sf")

# MAKE A MAP ===================================================================

# Get lat/lon ranges
message('Lat range: ',min(metadata_selected$lat),' - ',max(metadata_selected$lat))
message('Lon range: ',min(metadata_selected$lon),' - ',max(metadata_selected$lon))

# Make a basic map 
ggplot() +
  geom_sf(data=country_borders, fill=NA) +
  geom_point(data=metadata_selected, aes(x=lon,y=lat,color=archivetype)) +
  theme_minimal() +
  xlim(-180,-10) + ylim(0,82) +
  ggtitle(paste0('Locations of selected proxies (n=',nrow(metadata_selected),')'))

# MAKE A TIME SERIES ===========================================================

# Create a dataframe
ts_selected_df <- tidyTs(ts_selected,age.var = 'age')

# Filter the records
ts_selected_df2 <- ts_selected_df %>% 
  filter(between(geo_latitude,30,50),
         between(geo_longitude,-120,-80),
         interpretation1_variable == 'temperature',
         age <= 21000) %>% 
  group_by(paleoData_TSid) %>% 
  arrange(archiveType)

ggplot(ts_selected_df2, aes(x=age,y=paleoData_values,color=paleoData_TSid)) +
  geom_point()

#plotTimeseriesStack(ts_selected_df2)
#?plotTimeseriesStack
