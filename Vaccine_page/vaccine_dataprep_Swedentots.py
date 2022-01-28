# here is most data prep for the vaccine data (specific calculations for each graph can be found on other scripts)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime as dt
from datetime import timedelta

## Import and sort data from Folkhälsomyndigheten
## initially deal with data from first two doses

df_vacc = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade tidsserie",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

df_vacc["day"] = 4  # set day as Thursday (when public health data is updated)

df_vacc["date"] = df_vacc.apply(
    lambda row: dt.fromisocalendar(row["År"], row["Vecka"], row["day"]), axis=1
)

df_vacc = df_vacc.replace("| Sverige |", "Sweden")

df_vacc["Andel vaccinerade"] = df_vacc["Andel vaccinerade"].replace(
    ",", ".", regex=True
)

df_vacc["Procent vaccinerade"] = (df_vacc["Andel vaccinerade"].astype(float)) * 100

df_vacc_lan = df_vacc[
    ["date", "Region", "Antal vaccinerade", "Procent vaccinerade", "Vaccinationsstatus"]
]

# only need values for Sweden, so limit the data set

df_vacc = df_vacc_lan[(df_vacc_lan["Region"] == "Sweden")]

## Now data for 3rd dose
## may need to note that 'at least 2 doses COULD include 3rd dose'...

third_vacc_dose = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Dos 3 per åldersgrupp",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

third_vacc_dose = third_vacc_dose.replace("| Sverige |", "Sweden")

third_vacc_dose["Andel vaccinerade"] = third_vacc_dose["Andel vaccinerade"].replace(
    ",", ".", regex=True
)

third_vacc_dose["Procent vaccinerade"] = (
    third_vacc_dose["Andel vaccinerade"].astype(float)
) * 100

third_vacc_dose_lan = third_vacc_dose

third_vacc_dose = third_vacc_dose[(third_vacc_dose["Region"] == "Sweden")]

## Became evident that åldersgroup data for 1st two doses differs from tidseries data (the latter excludes totals for 12-15 year olds)
## Need something more comparable to third dose ideally so that we can make comparisons between 1/2 and third doses.

df_vacc_ålders = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade ålder",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

df_vacc_ålders = df_vacc_ålders.replace("| Sverige |", "Sweden")

df_vacc_ålders["Andel vaccinerade"] = df_vacc_ålders["Andel vaccinerade"].replace(
    ",", ".", regex=True
)

df_vacc_ålders["Procent vaccinerade"] = (
    df_vacc_ålders["Andel vaccinerade"].astype(float)
) * 100

df_vacc_ålders_lan = df_vacc_ålders

df_vacc_ålders = df_vacc_ålders[
    (df_vacc_ålders["Region"] == "Sweden") & (df_vacc_ålders["Åldersgrupp"] == "Totalt")
]

# take a population measure for each lan (to use in maps)

SCB_population = pd.read_excel(
    "https://blobserver.dckube.scilifelab.se/blob/SCB_pop_data.xlsx",
    sheet_name="Sheet 1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Need to get total population size of Sweden for use in calculations
# Take the sum of all the counties across Sweden

Swedish_population = SCB_population["Population"].sum()

# Import data for 3rd dose time series

third_timseries = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade tidsserie dos 3",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

third_timseries["day"] = 4  # set day as Thursday (when public health data is updated)

third_timseries["date"] = third_timseries.apply(
    lambda row: dt.fromisocalendar(row["År"], row["Vecka"], row["day"]), axis=1
)

third_timseries = third_timseries.replace("| Sverige |", "Sweden")

third_timseries = third_timseries[(third_timseries["Region"] == "Sweden")]

third_timseries = third_timseries[["date", "Region", "Antal vaccinerade"]]
