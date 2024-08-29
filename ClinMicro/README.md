> **Status:** Manually run whenever there is new data.

## Scripts related to clinical microbiology

This folder contains all of the scripts required to produce the visualisations shown on the [SARS-CoV-2 variants for Uppsala](https://www.pathogens.se/dashboards/variants_region_uppsala/) dashboard on the portal. The data are held offline. All of the scripts use the global requirements file for the visualisations repository that contains this subfolder.

**lineage_five_recent.py** - script to prepare the data and produce the graph for lineages classified according to their Pango lineage more granularly than in the 'four' lineage plot. Data are limited to the period since October 2023.

**lineage_four_recent.py** - script to prepare the data and produce the graph for lineages classified according to their Pango lineage. Data are limited to the period since the start of 2023.

**lineage_one_wholetime.py** - script to prepare the data and produce the graph for lineages classified according to their WHO classification and/or Pango lineage. Shows data from the full timeline.
