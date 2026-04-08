>**Status:** Historic, data not updated anymore.

## Count_publications

This folder contains the information required to create the plot related to counts of publications in the COVID-19 publication database and showed in [COVID-19 publication overview](https://www.pathogens.se/dashboards/covid_publications/) dashboard. It comprises of a combined line and bar plot. Note that this plot is set up in the dynamic repository to automatically update.

**count_publications.py** - the script used to produce the plot. Reads data from `Swedish_COVID19_publications_data.json`.

**gen_recent_pub.py** - the script used to produce table of recent publications. Reads data from `Swedish_COVID19_publications_data.json`.

**Swedish_COVID19_publications_data.json** - local copy of the publications data, previously fetched from `https://publications-covid19.scilifelab.se/publications.json` (now defunct).
