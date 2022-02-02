## map

This folder contains the files used to produce the map for the symptoms study (in dynamic as a cron job).

**gitignore** - a gitignore file for this part of the reporsitory.

**symptoms_map.py** - Script that produces versions of the symptoms map in both English and Swedish. The map prints in a .json file that saves in your directory.

**symptoms_map_English.py** - Script produces an English language version of the map for the symptom study. This map feeds into one in dynamic_cron and will re-run daily on the Portal (on dedicated page and home page).

**symptoms_map_Swedish.py** - Script produces an Swedish language version of the map for the symptom study. This map feeds into one in dynamic_cron and will re-run daily on the Portal (on dedicated page and home page).

**requirements.txt** - the requirements file used to recreate the environment needed to run the python script.

**sverige-lan-counties-of-sweden.geojson** - a geojson file showing the counties of Sweden. We now use the other geojson because this one is larger, but it could be useful in some cases as it has more detail in some respects. 

**sweden-counties.geojson** - a geojson file showing the counties of Sweden. This map is much smaller, but shows large water bodies well and provides sufficient data for our purposes.
