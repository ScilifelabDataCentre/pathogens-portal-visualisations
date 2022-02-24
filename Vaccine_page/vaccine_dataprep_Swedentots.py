# here is most data prep for the vaccine data (specific calculations for each graph can be found on other scripts)
# Graph scripts pull from here

import pandas as pd
import os
from datetime import datetime as dt
from datetime import timedelta

## Import and sort data from Folkhälsomyndigheten
## initially deal with data from first two doses

# df_vacc comprises time series data for the first two doses
# It can be used for calculating rates, totals, and time series plots

df_vacc = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade tidsserie",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# convert week date to full date

df_vacc["day"] = 1  # set day as Monday

df_vacc["date"] = df_vacc.apply(
    lambda row: dt.fromisocalendar(row["År"], row["Vecka"], row["day"]), axis=1
)

# We need to calculate values for the population. Don't use the values for just the population eligible for vaccination

df_vacc["Andel vaccinerade"] = df_vacc["Andel vaccinerade"].replace(
    ",", ".", regex=True
)

df_vacc["Procent vaccinerade"] = (df_vacc["Andel vaccinerade"].astype(float)) * 100

df_vacc_lan = df_vacc[
    [
        "date",
        "Region",
        "Antal vaccinerade",
        "Procent vaccinerade",
        "Vaccinationsstatus",
    ]
]

# REVIEW DOING THE LIMITATION HERE??
# First need to change the way that Sweden is written

df_vacc_lan = df_vacc_lan.replace("| Sverige |", "Sweden")

df_vacc = df_vacc_lan[(df_vacc_lan["Region"] == "Sweden")]

## Now timeseries data for 3rd dose

third_timseries = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade tidsserie dos 3",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Set date

third_timseries["day"] = 1  # set day as Monday

third_timseries["date"] = third_timseries.apply(
    lambda row: dt.fromisocalendar(row["År"], row["Vecka"], row["day"]), axis=1
)

# Limit data to just Sweden

third_timseries = third_timseries.replace("| Sverige |", "Sweden")

third_timseries = third_timseries[(third_timseries["Region"] == "Sweden")]

third_timseries["Procent vaccinerade"] = (
    third_timseries["Andel vaccinerade"].astype(float)
) * 100

third_timseries = third_timseries[
    ["date", "Region", "Antal vaccinerade", "Procent vaccinerade"]
]

# Now we are going to process data related to age

# Do first and second dose data first

df_vacc_ålders_lan = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade ålder",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Convert how Sweden is written
df_vacc_ålders_lan = df_vacc_ålders_lan.replace("| Sverige |", "Sweden")

#

df_vacc_ålders_lan["Andel vaccinerade"] = df_vacc_ålders_lan[
    "Andel vaccinerade"
].replace(",", ".", regex=True)

df_vacc_ålders_lan["Procent vaccinerade"] = (
    df_vacc_ålders_lan["Andel vaccinerade"].astype(float)
) * 100

# df_vacc_ålders_lan = df_vacc_ålders

# WHAT DO WE USE THIS FOR?! MAYBE LIMIT LIKE THIS IS BEST ELSEWHERE
df_vacc_ålders = df_vacc_ålders_lan[
    (df_vacc_ålders_lan["Region"] == "Sweden")
    & (df_vacc_ålders_lan["Åldersgrupp"] == "Totalt")
]

# Now process data for third dose

third_vacc_dose_lan = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Dos 3 per åldersgrupp",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

third_vacc_dose_lan = third_vacc_dose_lan.replace("| Sverige |", "Sweden")

third_vacc_dose_lan["Andel vaccinerade"] = third_vacc_dose_lan[
    "Andel vaccinerade"
].replace(",", ".", regex=True)

third_vacc_dose_lan["Procent vaccinerade"] = (
    third_vacc_dose_lan["Andel vaccinerade"].astype(float)
) * 100

# This used for livetext
third_vacc_dose = third_vacc_dose_lan[(third_vacc_dose_lan["Region"] == "Sweden")]


# Obtain population measures for Swedish population (number of people in country)
# We use this for the recalculations, so we can calculate vaccination as a percent of whole population

SCB_population = pd.read_excel(
    "https://blobserver.dckube.scilifelab.se/blob/SCB_pop_data.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# original data includes data for each lan
# Now we calculate whole population data

Swedish_population = SCB_population["Population"].sum()
