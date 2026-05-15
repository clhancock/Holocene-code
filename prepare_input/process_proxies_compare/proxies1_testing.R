#===============================================================================
# This package loads the proxy database and stores it in an easier-to-load format.
#  - https://nickmckay.org/lipdR/
#  - https://nickmckay.org/GeoChronR/articles/TsFilteringAndMapping.html
# author: Michael Erb
#===============================================================================

library(lipdR)
library(geoChronR)
library(ggplot2)
library(tidyverse)
library(data.table)

# LOAD PROXIES =================================================================

data_dir <- 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/more/'
#proxies_all <- readLipd(paste0(data_dir,'database/'))
#proxies_all <- readLipd(paste0(data_dir,'sample_100/'))
proxies_all <- readLipd(paste0(data_dir,'sample_1/'))
all_ts <- extractTs(proxies_all)
message('N proxies: ',length(proxies_all))
message('N timeseries: ',length(all_ts))

all_ts[1]
test = all_ts[[1]]$interpretation1_scope

counter = 0
new_ts = c()
for (i in 1:length(all_ts)) {
  if ('paleoData_values' %in% names(all_ts[[i]])) {
    counter = counter+1
    new_ts[[counter]] = all_ts[[i]]
  }  
}
print(counter)


for (i in 1:length(all_ts)) {
  if (all_ts[[i]]["paleoData_TSid"] == 'lcRkbtGT6LrW6s4NiuT') {
    print(i)
  }  
}

record = all_ts[[29]]

# PRINT METADATA ===============================================================

# Print data counts
var_name <- "archiveType"
print_counts <- function(selected_ts,var_name) {
  metadata_values <- pullTsVariable(selected_ts,var_name)
  metadata_values_df <- as.data.frame(metadata_values)
  colnames(metadata_values_df) <- c("var")
  count_metadata_values <- metadata_values_df %>% 
    count(var) %>% 
    arrange(desc(n))
  message(var_name,' - Total: ',nrow(metadata_values_df))
  print(count_metadata_values)
}

print_counts(all_ts,"dataSetName")
print_counts(new_ts,"dataSetName")

print_counts(all_ts,"paleoData_TSid")







datasetname = pullTsVariable(all_ts,"dataSetName")
np.unique


# SAVE DATA ====================================================================

# Create a dataframe with metadata
metadata_all <- data.frame(
  tsid        = pullTsVariable(all_ts,"paleoData_TSid"),
  datasetname = pullTsVariable(all_ts,"dataSetName"),
  primary     = pullTsVariable(all_ts,"paleoData_isPrimary"),
  variable    = pullTsVariable(all_ts,"paleoData_variableName"),
  lat         = pullTsVariable(all_ts,"geo_latitude"),
  lon         = pullTsVariable(all_ts,"geo_longitude"),
  archivetype = pullTsVariable(all_ts,"archiveType"),
  proxytype   = pullTsVariable(all_ts,"paleoData_proxy"),
  interpvar   = pullTsVariable(all_ts,"interpretation1_variable"),
  has_values  = !sapply(pullTsVariable(all_ts,"paleoData_values"), is.null),
  has_age     = !sapply(pullTsVariable(all_ts,"age"), is.null),
  has_year    = !sapply(pullTsVariable(all_ts,"year"), is.null)
)

# GET METADATA =================================================================

# Find records which meet the given criteria
ind_selected <- which(
  
  # Record has values
  metadata_all$has_values
  
  # Record has age or year
  & (metadata_all$has_age | metadata_all$has_year)
  
  # paleoData_isPrimary is TRUE or NA
  & (metadata_all$primary == "TRUE" | is.na(metadata_all$primary))
  
  # Record is in selected region
  & between(metadata_all$lat,0,85) & between(metadata_all$lon,-180,-10)
  
  # archiveType is not Midden
  & (metadata_all$archivetype != "Midden" | is.na(metadata_all$archivetype))
  
  # paleoData_proxy is not pollen
  & (metadata_all$proxytype != "pollen" | is.na(metadata_all$proxytype))
  
  # interpretation1_variable is a temperature or preciptiation variable
  & metadata_all$interpvar %in% c("temperature","effectivePrecipitation","precipitation")
  
  # Remove records that appear to be erroreous
  & !metadata_all$tsid %in% c("WEB33ffbfb3")
  
)

# Get the selected records and metadata
ts_selected <- all_ts[ind_selected]
metadata_selected <- metadata_all[ind_selected,]

