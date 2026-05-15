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

# LOAD PROXIES =================================================================

# Load the proxy data
data_dir <- 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
proxies_all <- readRDS(paste0(data_dir,'proxy_ts_2026-02-27.RData'))

# Extract the proxy time series
all_ts <- extractTs(proxies_all)

# MAKE A MAP ===================================================================

# Make a map
mapLipd(proxies_all, global = TRUE, size = 2) +
  ggtitle("Proxy records from dropbox")
#ggsave(paste0(data_dir,'map_proxies.png'))

# EXPLORE DATA 1 ===============================================================

# Get names of all terms in the dataset
n_ts <- length(all_ts)
terms_all <- c()
for (i in 1:n_ts) {
  terms_all[[i]] <- as.data.frame(names(all_ts[[i]]))
}

# Print a summary of the terms
terms_all_df <- do.call("rbind",terms_all)
colnames(terms_all_df) <- c("var")
count_terms <- terms_all_df %>% 
  count(var) %>% 
  arrange(desc(n))
message('Total datasets: ',n_ts)
View(count_terms)

rm(terms_all,terms_all_df)

# EXPLORE DATA 2 ===============================================================

# Print data counts
var_name <- "archiveType"
print_counts <- function(selected_ts,var_name) {
  metadata_values <- pullTsVariable(selected_ts,var_name)
  metadata_values_df <- as.data.frame(metadata_values)
  colnames(metadata_values_df) <- c("var")
  count_metadata_values <- metadata_values_df %>% 
    count(var) %>% 
    arrange(desc(n))
  print(count_metadata_values)
  #print(nrow(metadata_values_df))
}

print_counts(all_ts,"archiveType")
print_counts(all_ts,"paleoData_proxy")
print_counts(all_ts,"paleoData_units")
print_counts(all_ts,"ageUnits")
print_counts(all_ts,"paleoData_variableName")
#print_counts(all_ts,"paleoData_longName")
#print_counts(all_ts,"paleoData_summaryStatistic")
print_counts(all_ts,"paleoData_isPrimary")
print_counts(all_ts,"interpretation1_direction")  # Note: Alternate version with capital I
#print_counts(all_ts,"interpretation1_scope")      # Note: Alternate version with capital I
print_counts(all_ts,"interpretation1_seasonality")
print_counts(all_ts,"interpretation1_seasonalityGeneral")
print_counts(all_ts,"interpretation1_variable")        # Note: Alternate version with capital I
print_counts(all_ts,"interpretation1_variableDetail")  # Note: Alternate version with capital I

# Other potentially useful vars
# agesPerKyr, maxYear, minYear, geo_latitude,geo_longitude,
# paleoData_TSid,paleoData_summaryStatistic
