

#metadata_all <- metadata_all %>% 
#  replace_na(list(primary = 'NA',
#                  primary2 = 'NA')) %>% 
#  mutate(primary_primary2 = paste0(primary,'_',primary2))

#metadata_selected <- metadata_all %>% 
#  filter(interpvar == 'temperature')
#counts <- metadata_selected %>% 
#  count(primary_primary2)




tsid        = pullTsVariable(all_ts,"paleoData_TSid")
datasetname = pullTsVariable(all_ts,"dataSetName")
primary     = pullTsVariable(all_ts,"paleoData_isPrimary")

ind_selected <- which((metadata_all$primary == "TRUE" | is.na(metadata_all$primary)))
ts_selected <- all_ts[ind_selected]
metadata_selected <- metadata_all[ind_selected,]



print_counts(all_ts,"paleoData_isPrimary")
print_counts(ts_selected,"paleoData_isPrimary")





ind_selected <- which(
  
  (metadata_all$variable %like% "uncertainty"))

metadata_selected <- metadata_all[ind_selected,]



ind_selected <- which(
  
  # Record has values
  metadata_all$has_values
  
  # Record has age or year
  & (metadata_all$has_age | metadata_all$has_year)
  
  # paleoData_isPrimary is TRUE or NA
  & (metadata_all$primary == "TRUE" | is.na(metadata_all$primary))
  
  # variable is not equal to age, depth, or year, and does not contain "uncertainty" or "age-"
  & (!metadata_all$variable %in% c("age","depth","year"))
  
  # variable does not contain "uncertainty" or "age-"
  & (!metadata_all$variable %like% "uncertainty")
  & (!metadata_all$variable %like% "age-"))
#& (metadata_all$archivetype == "TerrestrialSediment")
#& (metadata_all$datasetname == "BiggsvilleCessfordQuarry.Baker.1989"))

ts_selected <- all_ts[ind_selected]
metadata_selected <- metadata_all[ind_selected,]

counts <- metadata_selected %>% 
  count(primary)
uncertainty <- metadata_selected %>% 
  filter(variable %like% "uncertainty")
uncertainty <- metadata_selected %>% 
  filter(variable == "uncertainty")

selected <- metadata_selected %>% 
  filter(archivetype == 'TerrestrialSediment')
counts2 <- selected %>% 
  count(datasetname)




# Create a dataframe with relevant metadata fields
metadata_all <- data.frame(
  archiveType     <- pullTsVariable(all_ts,"archiveType"),
  agesPerKyr      <- pullTsVariable(all_ts,"agesPerKyr"),
  maxYear         <- pullTsVariable(all_ts,"maxYear"),
  minYear         <- pullTsVariable(all_ts,"minYear"),
  paleoData_units <- pullTsVariable(all_ts,"paleoData_units"),
  geo_latitude    <- pullTsVariable(all_ts,"geo_latitude"),
  geo_longitude   <- pullTsVariable(all_ts,"geo_longitude"),
  ageUnits        <- pullTsVariable(all_ts,"ageUnits"),
  paleoData_TSid         <- pullTsVariable(all_ts,"paleoData_TSid"),
  paleoData_variableName <- pullTsVariable(all_ts,"paleoData_variableName"),
  paleoData_longName     <- pullTsVariable(all_ts,"paleoData_longName"),
  paleoData_summaryStatistic <- pullTsVariable(all_ts,"paleoData_summaryStatistic"),
  paleoData_isPrimary        <- pullTsVariable(all_ts,"paleoData_isPrimary"),
  interpretation1_scope      <- pullTsVariable(all_ts,"interpretation1_scope")
)
colnames(metadata_all) <- c('archiveType','agesPerKyr','maxYear','minYear','paleoData_units',
                            'geo_latitude','geo_longitude','ageUnits','paleoData_TSid','paleoData_variableName',
                            'paleoData_longName','paleoData_summaryStatistic','paleoData_isPrimary','interpretation1_scope')
