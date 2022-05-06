## RECOVAC

This folder contains all of the older scripts used for this project. This typically involves the production of individual plots, rather than combined plots.

**comorbidity_cases_dataprep.py** - script to prepare data related to the number of covid cases detected in patients with the comorbidities considered (cancer, cardiovascular disease, respiratory disease, and diabetes). Feeds into comorbidity_subplots_wbuttons.py (content of bottom subplot). A copy of that from the main repository that will not be updated, so that it will continue to work with the scripts here.

**comorbidity_cases_indivplots.py** - script produces separate plots for COVID cases among those with a comorbidity of interest (diabetes, cancer, respiratory disease, cardiovascular disease). Uses comorbidity_cases_dataprep.py,

**comorbidity_vaccinecov_dataprep.py** - script to prepare data related to vaccine coverage among patients with the comorbidities considered (cancer, cardiovascular disease, respiratory disease, and diabetes). Feeds into comorbidity_subplots_wbuttons.py (content of plot subplot). A copy of that from the main repository that will not be updated, so that it will continue to work with the scripts here.

**comorbidity_vaccinecov_indivplots** - script produces separate plots for vaccination coverage among those with a comorbidity of interest (diabetes, cancer, respiratory disease, cardiovascular disease). Uses comorbidity_vaccinecov_dataprep.py.

**requirements.txt** - requirements file showing packages used.

**Swedishpop_ICU_indivplots_noagecats.py** - script to produce an individual plot of ICU admission numbers among the Swedish population. The data is not subdivided into age categories.

**Swedishpop_ICU_indivplots.py** - script to produce individual plots of ICU admission numbers among the Swedish population. The data is subdivided into age categories.

**Swedishpop_vaccinecov_dataprep.py** - script to prepare the data related to vaccine coverage for each dose in the Swedish population. The prepared data is used by Swedishpop_vaccinecov_plotwbuttons.py. A copy of that from the main repository that will not be updated, so that it will continue to work with the scripts here.

**Swedishpop_vaccinecov_indivplots.py** - script to produce individual plots on vaccine coverage within the Swedish population. Data is subdivided by age category. Uses data from Swedishpop_vaccinecov_dataprep.py.