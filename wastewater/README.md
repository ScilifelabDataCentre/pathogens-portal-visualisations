>**Status:** Active, automatically run in `dc-dynamic`'s [runner_every10mins.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_every10mins.sh)

## wastewater

This folder contains all of the scripts and associated files required to produce the visualisations displayed on the wastewater page that were produced in plotly using python. The plots run directly on cron and are updated every 10 minutes. Remember to rebuild in cron if you update.

**Archive** - Contains old/historic script for reference.

**Data** - Contains sample data to test some scripts.

**combined_slu_influenza_a.py** - This script produces a graph with wastewater data from SLU for [influenza A](https://www.pathogens.se/dashboards/wastewater/influenza_quantification/).

**combined_slu_influenza_b.py** - This script produces a graph with wastewater data from SLU for [influenza B](https://www.pathogens.se/dashboards/wastewater/influenza_quantification/).

**combined_slu_regular.py** - This script produces a graph with wastewater data from SLU for [covid-19](https://www.pathogens.se/dashboards/wastewater/covid_quantification/covid_quant_slu/).

**interactive_wastewater_map.py** - Used to created the interactive map in the [wasterwater index](https://www.pathogens.se/dashboards/wastewater/) page.

**overall_site_table.py** - Used to created the overall site table in the [wasterwater index](https://www.pathogens.se/dashboards/wastewater/) page.

**slu_COVID_site_table.py** - Used to created the site table displayed in [SLU covid-19](https://www.pathogens.se/dashboards/wastewater/covid_quantification/covid_quant_slu/) page.

**slu_INF_site_table.py** - Used to created the site table displayed in [SLU influenza](https://www.pathogens.se/dashboards/wastewater/influenza_quantification/) page.

**slu_RSV_site_table.py** - Used to created the site table displayed in [SLU RSV](https://www.pathogens.se/dashboards/wastewater/rsv_quantification/) page.

**sweden-counties.geojson** - Underlying basemap geojson file, created using publicly available data from multiple sources. Used in `interactive_wastewater_map.py` script.



**NOTE:** The files in this repository contain commented out code towards the end that can be used to enable the figures to be output in different formats. The files are set so that they will print json when run. The scripts are 'fed into' runner scripts in the dynamic-cron repo to enable automatic updates directly on the Portal pages.
