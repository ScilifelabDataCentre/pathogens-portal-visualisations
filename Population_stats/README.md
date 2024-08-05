>**Status:** Still relavant as RECOVAC dashboard might be updated

# Swedish Population Summary

This repository contains the script that can be used to generate a summary of the Swedish population from publicly available data from https://www.scb.se/. The link required to obtain the most up to date data will change each quarter, so manual modifications will be required to that specific part of the script (the part related to data entry). The resultant summary excel file should be updated in blobserver [here](https://blobserver.dc.scilifelab.se/blob/SCB_pop_data.xlsx/info) for use in calculations related to the vaccinations and postcovid pages of the portal.

**Generate_population_summary.py** - A script that fetches population data from given URL, parse and generates a `xlsx` file which should be then uploaded to blobserver manually.
