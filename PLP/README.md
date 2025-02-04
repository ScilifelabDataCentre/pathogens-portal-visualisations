>**Status:** Historic, data is not updated

## PLP

This folder contains the two scripts required to produce the visualisations displayed on the [PLP Test project reporting page](https://www.pathogens.se/resources/integrative_outbreak_sim/).
The visualisations are produced with `Plotly` using `Python`.
The plots don't run on `cron` and won't be updated automatically,  as the data is already historical (generated during the project). Just remember to run the scripts manually in the unlikely event that there is an update.

**PLP-TEST-labs-analysis-phase-1.py** - This script produces a scatter plot of the labs activity, showing the number of actions taken per day during phase 1.

**PLP-TEST-labs-analysis-phase-2.py** - This script produces a timeline plot in the form of a Gantt chart, showing the labs activity and process over time.

**NOTE:** The files in this repository contain commented out code towards the end that can be used to enable the figures to be output in different formats. The files are set so that they will display the graphs in one's browser and save it to a json file as well. The resulting json files have to be uploaded to blobserver to be accessible by the Portal's page.
