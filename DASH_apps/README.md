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
