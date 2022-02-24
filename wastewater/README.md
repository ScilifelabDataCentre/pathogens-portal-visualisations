## wastewater

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the wastewater page that were produced in plotly using python.The plots run directly on cron and are updated every 10 minutes 

**combined_slu_logaxis.py** - This script produces a graph with wastewater data from SLU (combined graph) presented on a log axis.

**combined_slu_regular.py** - This script produces a graph with wastewater data from SLU (combined graph) presented on linear axes.

**combined_stockholm_logaxis.py** - This script produces a graph with wastewater data from Stockholm (combined graph) presented on a log axis.

**combined_stockhom_regular.py** - This script produces a graph with wastewater data from Stockholm (combined graph) presented on linear axes.

**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

**sweden-counties.geojson** - Underlying basemap geojson file, created using publicly available data from multiple sources.

**interactive_wastewater_map.py** - map currently under development. Will show ranked measures high/low/med at different sites. Currently uses fake data.

**NOTE:** The files in this repository contain commented out code towards the end that can be used to enable the figures to be output in different formats. The files are set so that they will print json when run. The scripts are 'fed into' runner scripts in the dynamic-cron repo to enable automatic updates directly on the Portal pages.
