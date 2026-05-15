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

# CREATE DATAFRAME WITH METADATA ===============================================

all_metadata <- data.frame(
  lat  = pullTsVariable(all_ts,"geo_latitude"),
  lon  = pullTsVariable(all_ts,"geo_longitude"),
  has_values = !sapply(pullTsVariable(all_ts,"paleoData_values"), is.null),
  has_age    = !sapply(pullTsVariable(all_ts,"age"), is.null),
  has_year   = !sapply(pullTsVariable(all_ts,"year"), is.null)
)

ind_selected <- which(
  all_metadata$has_values
  & (all_metadata$has_age | all_metadata$has_year))

# FILTERS ======================================================================

message('Total datasets: ',n_ts)

# Filter 1: Time series must have fields for paleoData_values and age or year
paleoData_values  <- pullTsVariable(all_ts,"paleoData_values")
age               <- pullTsVariable(all_ts,"age")
year              <- pullTsVariable(all_ts,"year")
ind_filter1 <- which(!sapply(paleoData_values, is.null) & (!sapply(age, is.null) | !sapply(year, is.null)))
all_ts_filter1 <- all_ts[ind_filter1]
n_ts_filter1 <- length(all_ts_filter1)
message('Filter 1, datasets remaining: ',n_ts_filter1)
rm(paleoData_values, age, year)

# Filter 2: primaryTimeseries is not False and var is not uncertainty, age, year, or depth
#print_counts(all_ts_filter1,"paleoData_isPrimary")
#print_counts(all_ts_filter1,"interpretation1_variable")
paleoData_isPrimary      <- pullTsVariable(all_ts_filter1,"paleoData_isPrimary")
interpretation1_variable <- pullTsVariable(all_ts_filter1,"interpretation1_variable")
ind_filter2 <- which(paleoData_isPrimary == "TRUE" | is.na(paleoData_isPrimary))
all_ts_filter2 <- all_ts_filter1[ind_filter2]
n_ts_filter2 <- length(all_ts_filter2)
message('Filter 2, datasets remaining: ',n_ts_filter2)

# Filter 3: Get proxies in the selected region
geo_latitude  <- pullTsVariable(all_ts_filter2,"geo_latitude")
geo_longitude <- pullTsVariable(all_ts_filter2,"geo_longitude")
message('Lat range: ',min(geo_latitude),', ',max(geo_latitude))
message('Lon range: ',min(geo_longitude),', ',max(geo_longitude))
ind_filter3 <- which(between(geo_latitude,0,85) & between(geo_longitude,-180,-10))
all_ts_filter3 <- all_ts_filter2[ind_filter3]
n_ts_filter3 <- length(all_ts_filter3)
message('Filter 3, datasets remaining: ',n_ts_filter3)

# Filter 4: Remove pollen and middens
#print_counts(all_ts_filter3,"archiveType")
#print_counts(all_ts_filter3,"paleoData_proxy")
archiveType     <- pullTsVariable(all_ts_filter3,"archiveType")
paleoData_proxy <- pullTsVariable(all_ts_filter3,"paleoData_proxy")
ind_filter4 <- which((archiveType != "Midden" | is.na(archiveType)) &
                       (paleoData_proxy != "pollen" | is.na(paleoData_proxy)))
all_ts_filter4 <- all_ts_filter3[ind_filter4]
n_ts_filter4 <- length(all_ts_filter4)
message('Filter 4, datasets remaining: ',n_ts_filter4)

# Filter 5: Get temperature and precipitation records
print_counts(all_ts_filter4,"interpretation1_variable")
interpretation1_variable <- pullTsVariable(all_ts_filter4,"interpretation1_variable")
ind_filter5 <- which(interpretation1_variable %in% c("temperature","effectivePrecipitation","precipitation"))
all_ts_filter5 <- all_ts_filter4[ind_filter5]
n_ts_filter5 <- length(all_ts_filter5)
message('Filter 5, datasets remaining: ',n_ts_filter5)

# Filter 6: Remove short records and records without valid data

# Filter 7: Remove records that appear to be erroneous


# ADD UNCERTAINTY VALUES =======================================================

