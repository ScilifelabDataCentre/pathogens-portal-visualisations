## postCOVID

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the postcovid page.

**SCB_pop_data.xlsx** - This is a copy of the most recent population data for Swedish counties taken from [SCB's population statistics page](https://www.scb.se/en/finding-statistics/statistics-by-subject-area/population/population-composition/population-statistics/).

**postcovid_dataprep.py** - script required to complete the data manipulations required for the plots. The resultant excel file should be uploaded to the blob server. It is used by the other plots from there.

**postcovid_mapfig_cases_U089.py** - script produces a map displaying the number of U089 postcovid syndrome diagnoses as a percentage of postcovid cases up to the current time period. Need to update week number here (aim to automate later).

**postcovid_mapfig_cases_U099.py** - script produces a map displaying the number of U099 postcovid syndrome diagnoses as a percentage of postcovid cases up to the current time period. Need to update week number here (aim to automate later).

**postcovid_mapfig_population_U089.py** - script produces a map displaying the number of U089 postcovid syndrome diagnoses as a percentage of the population up to the current time period.

**postcovid_mapfig_population_U099.py** - script produces a map displaying the number of U099 postcovid syndrome diagnoses as a percentage of the population up to the current time period.

**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

**sweden-counties.geojson** - a geojson file showing the counties of Sweden. This map is much smaller, but shows large water bodies well and provides sufficient data for our purposes.
