# Covid_portal_vis

This repository holds the inital visualisation scripts produced for the COVID-19 data portal, and some other scripts for plots under development. Some of the scripts here are also used in the dynamic repository, where they are used in cron jobs so that the plots update automatically.

## Collaborations 

This plot has not been used in the portal so far, but could be used to establish a circos plot.

## Count_publications

This file contains the information required to create the plot related to counts of publications in the COVID-19 publication database. It comprises of a combined line and bar plot. Note that this plot is set up in the dynamic repository to automatically update.

**gitignore** - a gitignore file for this part of the reporsitory.
**count_publications.py** - the script used to produce the plot.
**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

## DASH_apps

This repository contains the initial scripts and associated files required to produce a DASH app (under development). This could be used as initial starting point for future DASH apps.

**assets folder** - contains the stylesheet used for the app. Important to include style sheets here so that the DASH app can locate and apply them.
**Dockerfile** - used to enable automatic updates in rendering.
**requirements.txt** - the requirements file used to recreate the environment needed to run the python scripts.
**sweden-counties.geojson** - a geojson file containing the data required to produce a map of the counties (lan) of Sweden.
**symptoms_map_date.py** - a simple DASH app in which users can select the date of symptoms data to be displayed on the map.
**symptoms_map_today.py** - a simple DASH app in which the latest symptoms data is displayed on the a map of Sweden.
**symptoms_map_today_eng.py** - a simple DASH app in which the latest symptoms data is displayed on the a map of Sweden, with English labels.
**try_add_tabs.py** - an initial draft of a DASH app using publilcly available data linked to COVID-19 cases.

## Tables

This file contains the information required to create the a table in plotly python. Tables in the portal are currently done using html.

**gitignore** - a gitignore file for this part of the reporsitory.
**recent_ten.py** - a script used to produce a table showing the 10 most recent publications in the COVID-19 publications database.
**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.




The wordcloud folder contains python script that can be used to generate a 'live' word cloud from the Covid-19 publications data. It also includes the font to be used as standard for the portal, a square shape that can be used as the 'mask' for the wordcloud (mask defines the shape) and a folder of example wordclouds. 

COUNT PUBLICATIONS

This folder contains the code used to produce 'live' counts of the cumulative number of publications in the COVID-19 publications database and the total number of publications added in each month. These are included as a line and bar plot on the same graph, respectively. 