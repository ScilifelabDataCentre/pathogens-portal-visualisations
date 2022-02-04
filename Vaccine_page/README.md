## Vaccine_page

This folder contains all the initial files required to produce the visualisations shown on the vaccines page on the portal.

**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

**sverige-kommuner-municipalities-of-sweden-2_LHmod_v2.json** - a json file used to produce a map of Swedish kommuns (for potential later use). This map was produced using data from multiple publicly available data sources.

**sweden-counties.geojson** - a geojson file containing the data required to produce a map of the counties (lan) of Sweden. Produced using data from publicly available data sources.

**vaccine_dataprep_Swedentots.py** - this script completes data manipulations necessary. No manual updates are required and the script does not need to be run itself (the other scripts will pull what they need from it).

**vaccine_heatmaps.py** - this script is used to produce a heatmaps of vaccine data related to coverage for each dose in each age-group. Uses publicly available information. It produces both the 'small' heatmap for the front page, and the 'standard' heatmap for the vaccines page itself.

**vaccine_indicator_barchart.py** - this script produces the barchart that compares the two methods of calculation (i.e. the calulcation based on who is 'eligible' in the population and 'the whole population').

**vaccine_livetext.py** - this script produces the key values that will be used to produce the dynamic text for the portal vaccines page.

**vaccine_maps_population.py** - this script produces maps of coverage according to Swedish lan. It produces all three maps used on the vaccine page.

**vaccine_timeseries_barchart.py** - this script produces the bar chart of the percentage of the population vaccinated over time.
