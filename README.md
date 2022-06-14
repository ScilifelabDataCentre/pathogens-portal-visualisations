# Covid_portal_vis

This repository holds the inital visualisation scripts produced for the COVID-19 data portal, and some other scripts for plots under development. Some of the scripts here are also used in the dynamic repository, where they are used in cron jobs so that the plots update automatically.

## Count_publications

This folder contains the code used to produce 'live' counts of the cumulative number of publications in the COVID-19 publications database and the total number of publications added in each month. These are included as a line and bar plot on the same graph, respectively. 

## DASH_apps

This folder contains files related to DASH apps. There are some basic scripts just showing maps (one that allows date selection) and there is also a draft app with tabs that includes some more advanced functions.

## Population_stats

This repository contains the script that can be used to generate a summary of the Swedish population from publicly available data from https://www.scb.se/. The data is updated each quarter, but not on a consistent date. The script generates a summary excel file should be updated in blobserver [here](https://blobserver.dckube.scilifelab.se/blob/SCB_pop_data.xlsx/info) for use in calculations related to the vaccinations and postcovid pages of the portal.

## RECOVAC

This folder contains all of the scripts and associated data required to produce the visualisations on the RACOVAC page of the portal. It includes bar charts and area under the curve plots. The data are provided by the RECOVAC project.

## Vaccine_page

This folder contains all of the scripts and associated data required to produce the visualisations on the vaccines page of the portal. It includes bar charts, heatmaps and choropleth maps. 

## Wordcloud

The wordcloud folder contains python script that can be used to generate a 'live' word cloud from the Covid-19 publications data. It also includes the font to be used as standard for the portal, a square shape that can be used as the 'mask' for the wordcloud (mask defines the shape) and a folder of example wordclouds. 

## map

This folder contains the scripts and associated files required to produce the choropleth maps used to display  the data from the symptoms app on the portal.

## postCOVID

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the postcovid page of the portal. The folder contains scripts to complete data manipulations and produce choropleth maps.

## wastewater

This folder contains all of the plots on the wastewater page that were created using plotly in python. This includes the 'combined' graphs, showing data from multiple areas displayed on both a linear and log scale.
