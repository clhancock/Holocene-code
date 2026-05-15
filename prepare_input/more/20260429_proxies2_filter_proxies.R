#===============================================================================
# This package loads the proxy database so it can be explored and filtered.
# Tutorials:
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

# Load the proxy data
data_dir <- 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
data_date <- '2026-02-27'
proxies_all <- readRDS(paste0(data_dir,'proxy_ts_',data_date,'.RData'))

# Extract the proxy time series
all_ts <- extractTs(proxies_all)

# MAKE A MAP ===================================================================

# Make a map
mapLipd(proxies_all, global = TRUE, size = 2) +
  ggtitle("Proxy records from dropbox")
#ggsave(paste0(data_dir,'map_proxies.png'))

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

#print_counts(all_ts,"archiveType")
#print_counts(all_ts,"paleoData_proxy")
#print_counts(all_ts,"paleoData_units")
#print_counts(all_ts,"ageUnits")
#print_counts(all_ts,"paleoData_variableName")
#print_counts(all_ts,"paleoData_longName")
#print_counts(all_ts,"paleoData_summaryStatistic")
#print_counts(all_ts,"paleoData_isPrimary")
#print_counts(all_ts,"interpretation1_direction")  # Note: Alternate version with capital I
#print_counts(all_ts,"interpretation1_scope")      # Note: Alternate version with capital I
#print_counts(all_ts,"interpretation1_seasonality")
#print_counts(all_ts,"interpretation1_seasonalityGeneral")
#print_counts(all_ts,"interpretation1_variable")        # Note: Alternate version with capital I
#print_counts(all_ts,"interpretation1_variableDetail")  # Note: Alternate version with capital I

# Other potentially useful vars
# agesPerKyr, maxYear, minYear, geo_latitude,geo_longitude,
# paleoData_TSid,paleoData_summaryStatistic

# CREATE DATAFRAME WITH METADATA ===============================================

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

# FILTER DATA 1 ================================================================

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

# FILTER DATA 2 ================================================================

# Loop through all records
record_length_all <- c()
n_selected <- length(ts_selected)
i <- 1
for (i in 1:n_selected) {
  #
  # If ages are missing, create an age column using the year column
  record_names <- names(ts_selected[[i]])
  if (!"age" %in% record_names) {
    message('NOTE: Adding age values from year values for record ',i)
    ts_selected[[i]]$age <- 1950 - ts_selected[[i]]$year
  }
  #
  # Get data and ages
  proxy_data <- ts_selected[[i]]$paleoData_values
  proxy_ages <- ts_selected[[i]]$age
  #
  # Compute record length
  ind_valid <- is.finite(proxy_data) & is.finite(proxy_ages)
  proxy_data_valid <- proxy_data[ind_valid]
  proxy_ages_valid <- proxy_ages[ind_valid]
  record_length <- max(proxy_ages_valid) - min(proxy_ages_valid)
  record_length_all[[i]] <- record_length
  #
}

# Add to dataframe
metadata_selected$record_length <- record_length_all

# Find records which meet the given criteria
ind_selected2 <- which(record_length_all >= 2500)

# Get the selected records and metadata
ts_selected <- ts_selected[ind_selected2]
metadata_selected <- metadata_selected[ind_selected2,]

# ADD UNCERTAINTY VALUES =======================================================

primary     = pullTsVariable(ts_selected[1],"paleoData_isPrimary")
pullTsVariable(ts_selected[2],"paleoData_isPrimary")
# SAVE RECORDS =================================================================

# Save filtered data
saveRDS(ts_selected,file=paste0(data_dir,'selected_ts_',data_date,'.RData'))
saveRDS(metadata_selected,file=paste0(data_dir,'selected_metadata_',data_date,'.RData'))

