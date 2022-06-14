## postCOVID

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the postcovid page.

**create_accomp_diagnoses.py** - script used to produce the json file underlying the 'accompanying diagnoses table' - this is the English language version.

**create_accomp_diagnoses_swe.py** - script used to produce the json file underlying the 'accompanying diagnoses table' - this is the Swedish language version.

**create_agesex_distcases.py** - script used to produce the barplots showing cumulative numbers of diagnoses divided by sex and age group category.

**postcovid_dataprep.py** - script required to complete the data manipulations required for the plots. The resultant excel file is uploaded to blob server. It is used by the other plots from there.

**postcovid_mapfig_cases_U089.py** - script produces a map displaying the number of U089 postcovid syndrome diagnoses as a percentage of postcovid cases up to the current time period.

**postcovid_mapfig_cases_U099.py** - script produces a map displaying the number of U099 postcovid syndrome diagnoses as a percentage of postcovid cases up to the current time period.

**postcovid_mapfig_population_U089.py** - script produces a map displaying the number of U089 postcovid syndrome diagnoses as a percentage of the population up to the current time period.

**postcovid_mapfig_population_U099.py** - script produces a map displaying the number of U099 postcovid syndrome diagnoses as a percentage of the population up to the current time period.

**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

**sweden-counties.geojson** - a geojson file showing the counties of Sweden. Used to produce the choropleth maps shown on the page. Used in the scripts related to the production of those maps.

**weeklycontacts_healthcare.py** - script used to produce file plot related to healthcare contacts divided only by diagnosis, NOT patient sex.

**weeklycontacts_healthcare_divsex.py** - script used to produce file plots related to healthcare contacts divided by patient sex.

**weeklycontacts_healthcare_small.py** - script used to produce file plot related to healthcare contacts divided only by diagnosis, NOT patient sex. This is a smaller version that is used for the home page of the portal.
