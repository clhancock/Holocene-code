# ADD UNCERTAINTY VALUES FOR TEMPERATURE =======================================

#TODO: If this is useful, work on it here.

# Reference table from Kaufman et al., 2020, slightly reordered:
# Archive type      | Proxy type      | Summer | Winter | Annual
# ------------------|-----------------|--------|--------|--------
# Marine sediment   | alkenone        |        |        | 1.7
# Marine sediment   | d18O            |        |        | 2.1
# Marine sediment   | Mg/Ca           | 1.9    | 1.9    | 1.9
# Marine sediment   | foraminifera    | 1.3    | 1.4    | 1.3
# Marine sediment   | dinocyst        | 1.7    | 1.2    | 1.2
# Marine sediment   | radiolaria      | 1.2    |        | 
# Multiple archives | TEX86           |        |        | 2.3
# Multiple archives | diatom          | 1.1    |        | 
# Multiple archives | pollen          | 2.0    | 3.0    | 2.1
# Multiple archives | GDGT            |        |        | 2.9
# Multiple archives | stable isotopes |        |        | default
# Lake sediment     | various         |        |        | default
# Lake sediment     | chironomid      | 1.4    |        | 
# Glacier ice       | various         |        |        | default
# Midden            | macrofossils    |        |        | default
# Wood              | tree ring width |        |        | default

# Print current temperature uncertainties
metadata_temp <- metadata_selected |> 
  filter(variable == "temperature", temp_uncer == "NA")

temp_proxy_types <- metadata_temp |> 
  count(proxytype) |> 
  arrange(desc(n))

for (type in temp_proxy_types$proxytype) {
  uncertainties <- metadata_temp |> 
    filter(proxytype == type) |> 
    count(temp_uncer)  
  message("=== ",type," ===")
  print(uncertainties)
}

# Print metadata
print_counts(ts_selected,"paleoData_variableName")
print_counts(ts_selected,"archiveType")
print_counts(ts_selected,"paleoData_proxy")
print_counts(ts_selected,"interpretation1_seasonality")
print_counts(ts_selected,"paleoData_temperature12kUncertainty")

# Loop through all records
i <- 1
n_added <- 0
for (i in 1:length(ts_selected)) {
  
  # Get metadata
  record_variable <- ts_selected[[i]]$paleoData_variableName
  record_archive  <- ts_selected[[i]]$archiveType
  record_proxy    <- ts_selected[[i]]$paleoData_proxy
  record_season   <- ts_selected[[i]]$interpretation1_seasonality
  record_uncer    <- ts_selected[[i]]$paleoData_temperature12kUncertainty
  if (is.null(record_variable)) {record_variable = "NA"}
  if (is.null(record_archive))  {record_archive = "NA"}
  if (is.null(record_proxy))    {record_proxy = "NA"}
  if (is.null(record_season))   {record_season = "NA"}
  if (is.null(record_uncer))    {record_uncer = "NA"}
  
  # If the record isn't temperature or already has uncertainty, go to the next one
  if (!record_variable == "temperature") {next}
  if (!record_uncer == "NA") {next}

  # Otherwise, see if it matches any of the criteria above
  
  # Marine sediments
  if (record_archive == "MarineSediment") {
    if ((record_proxy == 'alkenone') & (record_season == 'annual')) {record_uncer <- 1.7; n_added <- n_added + 1}
    if ((record_proxy == 'd18o') & (record_season == 'annual'))     {record_uncer <- 2.1; n_added <- n_added + 1}
    if (record_proxy == 'mg/ca')                                    {record_uncer <- 1.9; n_added <- n_added + 1}
    if (record_proxy == 'foraminifera') {
      if (record_season == 'summer') {record_uncer <- 1.3; n_added <- n_added + 1}
      if (record_season == 'winter') {record_uncer <- 1.4; n_added <- n_added + 1}
      if (record_season == 'annual') {record_uncer <- 1.3; n_added <- n_added + 1}
    }
    if (record_proxy == 'dinocyst') {
      if (record_season == 'summer') {record_uncer <- 1.7; n_added <- n_added + 1}
      if (record_season == 'winter') {record_uncer <- 1.2; n_added <- n_added + 1}
      if (record_season == 'annual') {record_uncer <- 1.2; n_added <- n_added + 1}
    }        
    if ((record_proxy == 'radiolaria') & (record_season == 'summer')) {record_uncer <- 2.3; n_added <- n_added + 1}
  }
  
  # Multiple archives
  if ((record_proxy == 'tex86') & (record_season == 'annual'))      {record_uncer <- 1.2; n_added <- n_added + 1}
  if ((record_proxy == 'diatom') & (record_season == 'summer'))     {record_uncer <- 1.1; n_added <- n_added + 1}
  if (record_proxy == 'pollen') {
    if (record_season == 'summer') {record_uncer <- 2.0; n_added <- n_added + 1}
    if (record_season == 'winter') {record_uncer <- 3.0; n_added <- n_added + 1}
    if (record_season == 'annual') {record_uncer <- 2.1; n_added <- n_added + 1}
  }        
  if ((record_proxy == 'gdgt') & (record_season == 'annual')) {record_uncer <- 2.9; n_added <- n_added + 1}

  # Lake sediments
  if (record_archive == 'lakesediment') {
    if (record_season == 'summer') {record_uncer <- 2.0; n_added <- n_added + 1}
    if (record_season == 'winter') {record_uncer <- 3.0; n_added <- n_added + 1}
    if (record_season == 'annual') {record_uncer <- 2.1; n_added <- n_added + 1}
  }        
}

message('Uncertainties added to ',n_added,' records!')
#_,_,_,_ = list_archive_proxy_season_uncertainty(proxy_ts_temp,'AFTER ADDING UNCERTAINTIES - ')
