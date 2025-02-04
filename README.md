# Pathogens portal visualisation

This repository holds the inital visualisation scripts produced for the [Swedish Pathogens Portal](https://pathogens.se), and some other scripts for plots under development. Some of the scripts here are also used in the dynamic repository, where they are used in cron jobs so that the plots update automatically.

## Archive

This folder contains old code that are not used anymore, but kept for reference if needed.

## ClinMicro

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the [SARS-CoV-2 variants](https://www.pathogens.se/dashboards/variants_region_uppsala/) dashboard, that were produced in plotly using python.

**Status:** Active, manually run whenever there is new data.

## Count_publications

This folder contains the code used to produce 'live' counts of the monthly cumulative number of publications in the [COVID-19 publication overview](https://www.pathogens.se/dashboards/covid_publications/) dashboard. These are included as a line and bar plot on the same graph, respectively.

**Status:** Active, automatically run in `dc-dynamic`'s [runner_weekly.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_weekly.sh)

## map

This folder contains the scripts and associated files required to produce the choropleth maps used to display the data from the symptoms app on the [Symptoms study](https://www.pathogens.se/dashboards/symptom_study_sweden/) dashboard.

**Status:** Historic, data not updated anymore

## npctests

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the [NPC test statistics](https://www.pathogens.se/dashboards/npc-statistics/) dashboard, that were produced in plotly using python.

**Status:** Historic, data not updated anymore

## PLP

This folder contains the scripts that produce both visualisations on the [PLP Test project reporting page](https://www.pathogens.se/resources/integrative_outbreak_sim/) of the portal.
It includes a scatter plot of labs activity for the first phase, and a timeline plot in a gantt chart style for the second phase.
The data was supplied by the labs participating in the PLP Test project.

**Status:** Historic, data is not updated

## Population_stats

This repository contains the script that can be used to generate a summary of the Swedish population from publicly available data from https://www.scb.se/. The data is updated each quarter, but not on a consistent date. The script generates a summary excel file should be updated in blobserver [here](https://blobserver.dc.scilifelab.se/blob/SCB_pop_data.xlsx/info) for use in calculations related to the vaccinations and postcovid pages of the portal.

**Status:** Still relavant as RECOVAC dashboard might be updated

## postCOVID

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the [postcovid](https://www.pathogens.se/dashboards/post_covid/) dashboard of the portal. The folder contains scripts to complete data manipulations and produce choropleth maps.

**Status:** Historic, data not updated anymore

## RECOVAC

This folder contains all of the scripts and associated data required to produce the visualisations on the [RECOVAC](https://www.pathogens.se/dashboards/recovac/) dashboard of the portal. It includes bar charts and area under the curve plots. The data are provided by the RECOVAC project.

**Status:** Active, manually run whenever there is new data.

## serology

This folder contains all of the scripts and associated data required to produce the visualisations on the [serology tests](https://www.pathogens.se/dashboards/serology-statistics/) dashboard of the portal. It includes bar charts and area under the curve plots. The data are provided by the SciLifeLab Autoimmunity and Serology Profiling unit.

**Status:** Active, automatically run in `dc-dynamic`'s [runner_every10mins.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_every10mins.sh)

## Vaccine_page

This folder contains all of the scripts and associated data required to produce the visualisations on the [vaccine administration](https://www.pathogens.se/dashboards/vaccines/) dashboard of the portal. It includes bar charts, heatmaps and choropleth maps.

**Status:** Historic, data not updated anymore

## wastewater

This folder contains all of the plots on the [wastewater](https://www.pathogens.se/dashboards/wastewater/) page that were created using plotly in python. This includes the 'combined' graphs, showing data from multiple areas displayed on both a linear and log scale.

**Status:** Active, automatically run in `dc-dynamic`'s [runner_every10mins.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_every10mins.sh)

## Wordcloud

The wordcloud folder contains python script that can be used to generate a 'live' word cloud from the Covid-19 publications data, which is used in [COVID-19 publication overview](https://www.pathogens.se/dashboards/covid_publications/) dashboard. It also includes the font to be used as standard for the portal, a square shape that can be used as the 'mask' for the wordcloud (mask defines the shape) and a folder of example wordclouds.

**Status:** Active, automatically run in `dc-dynamic`'s [runner_weekly.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_weekly.sh)
