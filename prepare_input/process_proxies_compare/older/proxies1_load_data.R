#===============================================================================
# This package loads the proxy database and stores it in an easier-to-load format.
#  - https://nickmckay.org/lipdR/
#  - https://nickmckay.org/GeoChronR/articles/TsFilteringAndMapping.html
# author: Michael Erb
#===============================================================================

library(lipdR)
library(geoChronR)
library(tidyverse)

# LOAD PROXIES =================================================================

data_dir <- 'C:/Users/erbm/Documents/data_climate/data_paleoclimate/proxies/dropbox/'
proxies_all <- readLipd(paste0(data_dir,'sample_10/'))

# Extract the proxy time series
all_ts <- extractTs(proxies_all)

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


n_records <- nrows(all_ts)
for (i in 1:62) {
  message(i,' - ',all_ts[[i]]$paleoData_TSid)
  
}

test40 <- all_ts[[40]]
test41 <- all_ts[[41]]
test42 <- all_ts[[42]]


print_counts(all_ts,"paleoData_TSid")
variable = pullTsVariable(all_ts,"paleoData_TSid")


print_counts(all_ts,"archiveType")
print_counts(all_ts,"paleoData_variableName")


print_counts(all_ts,"paleoData_proxy")
print_counts(all_ts,"paleoData_units")
print_counts(all_ts,"ageUnits")
#print_counts(all_ts,"paleoData_longName")
#print_counts(all_ts,"paleoData_summaryStatistic")
print_counts(all_ts,"paleoData_isPrimary")
print_counts(all_ts,"interpretation1_direction")  # Note: Alternate version with capital I
#print_counts(all_ts,"interpretation1_scope")      # Note: Alternate version with capital I
print_counts(all_ts,"interpretation1_seasonality")
print_counts(all_ts,"interpretation1_seasonalityGeneral")
print_counts(all_ts,"interpretation1_variable")        # Note: Alternate version with capital I
print_counts(all_ts,"interpretation1_variableDetail")  # Note: Alternate version with capital I

# Filter -----------------------------------------------------------------------

variable = pullTsVariable(all_ts,"paleoData_variableName")
selected_ts = all_ts[variable == 'temperature']

print_counts(selected_ts,"archiveType")
print_counts(selected_ts,"paleoData_variableName")
print_counts(selected_ts,"paleoData_proxy")
print_counts(selected_ts,"paleoData_units")
print_counts(selected_ts,"ageUnits")
#print_counts(selected_ts,"paleoData_longName")
#print_counts(selected_ts,"paleoData_summaryStatistic")
print_counts(selected_ts,"paleoData_isPrimary")
print_counts(selected_ts,"interpretation1_direction")  # Note: Alternate version with capital I
#print_counts(selected_ts,"interpretation1_scope")      # Note: Alternate version with capital I
print_counts(selected_ts,"interpretation1_seasonality")
print_counts(selected_ts,"interpretation1_seasonalityGeneral")
print_counts(selected_ts,"interpretation1_variable")        # Note: Alternate version with capital I
print_counts(selected_ts,"interpretation1_variableDetail")  # Note: Alternate version with capital I
