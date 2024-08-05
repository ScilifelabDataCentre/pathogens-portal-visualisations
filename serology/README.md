>**Status:** Active, automatically run in `dc-dynamic`'s [runner_every10mins.sh](https://github.com/ScilifelabDataCentre/dc-dynamic/blob/master/runner_every10mins.sh)

## Serology

This folder contains the two scripts required to produce the visualisations displayed on the serology dashboard page.
The visualisations are produced with `Plotly` using `Python`.
The plots run directly on `cron` and are updated every 10 minutes. Remember to rebuild in `cron` if you update.

**weekly-serology-tests.py** - This script produces a bar graph with serology data from the SciLifeLab Autoimmunity and Serology Profiling unit.

**cumulative-serology-tests.py** - This script produces a cumulative line graph with serology data from the SciLifeLab Autoimmunity and Serology Profiling unit.

**NOTE:** The files in this repository contain commented out code towards the end that can be used to enable the figures to be output in different formats. The files are set so that they will print json when run. The scripts are 'fed into' runner scripts in the dynamic-cron repo to enable automatic updates directly on the Portal pages.

**Development:** Poetry was used for dependency managagement here, and relies on the `pyproject.toml` and `poetry.lock` files for this.

As per PEP-518 and PEP-517, `pyproject.toml` became the de facto standard for project management in python and its format is supported by pip.
Hence, while I recommend using poetry with the provided `poetry.lock` file to 1:1 reproduce this development environment, you can also run `pip install pyproject.toml` if you want to quickly test it.
