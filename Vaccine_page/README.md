## Vaccine_page

This folder contains all the initial files required to produce the visualisations shown on the vaccines page on the portal.

**SCB_pop_data.xlsx** - This is a copy of the most recent population data for Swedish counties taken from [SCB's population statistics page](https://www.scb.se/en/finding-statistics/statistics-by-subject-area/population/population-composition/population-statistics/).

**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

**sverige-kommuner-municipalities-of-sweden-2_LHmod_v2.json** - a json file used to produce a map of Swedish kommuns (for potential later use). This map was produced using data from multiple publicly available data sources.

**sweden-counties.geojson** - a geojson file containing the data required to produce a map of the counties (lan) of Sweden.

**vaccine_dataprep_Swedentots.py** - this script completes data manipulations necessary to produce accurate data manipulations. Currently requires a manual update if links to the data should change and the manual addition of the latest total population size for Sweden (may adjust to occur automatically in future).

**vaccine_gauge.py** - this script could be used to produce a gauge and associated indicator data using publicly available data related to vaccines.

**vaccine_heatmap.py** - this script is used to produce a heatmap of vaccine data related to coverage for each dose in each age-group. Uses publicly available information.

**vaccine_indicator_panel_content.py** - this script produces the key values that will be used as indicators on the vaccines web page.

**vaccine_maps_FoHM.py** - this script produces maps of coverage according to Swedish lan. It uses publicly available data from FoHM.

**vaccine_maps_population.py** - this script produces maps of coverage according to Swedish lan. It uses publicly available data from FoHM adjusted for the entire population (minor change from FoHM clauclations).

**vaccine_timeseries_barchart.py** - this script uses the FoHM data related to the number of vaccines given over time to produce a timeseries of the coverage of the first and second doses (for the whole of Sweden).
