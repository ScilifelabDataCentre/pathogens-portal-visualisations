>**Status:** Active, automatically run in `dc-dynamic`'s [runner_weekly.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_weekly.sh)

## Wordcloud

This folder contains all the files required to produce the wordclouds shown on the [COVID-19 publication overview](https://www.pathogens.se/dashboards/covid_publications/) dashboard. These scripts are used directly in cron jobs, so updating them will directly affect the visualisations on the portal. Remember to rebuild cron after an update here, or the update will not work.

**examplewordclouds folder** - This folder contains images of some example wordclouds.

**IBMPlexSabs-Bold.ttf** - the typeface used in wordclouds.

**SciLifeLab_symbol_POS_rectangle.png** - used to produce a rectangular shaped 'mask' for wordclouds, use this to make wordclouds in a rectangle shape.

**SciLifeLab_symbol_POS_square.png** - used to produce a square shaped 'mask' for wordclouds, use this to make wordclouds in a square shape.

**livewordcloud.py** - produces the wordclouds images.
