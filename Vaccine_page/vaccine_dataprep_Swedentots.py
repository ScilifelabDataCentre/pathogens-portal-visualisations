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
#


def get_vaccination_data(
    data_url, sheet_name, set_date=False, only_sweden=False, needed_columns=None
):
    df_vacc = pd.read_excel(
        data_url,
        sheet_name=sheet_name,
        header=0,
        engine="openpyxl",
        keep_default_na=False,
    )

    # if needed, convert week date to full date, initially set day as Monday
    if set_date:
        df_vacc["day"] = 1
        df_vacc["date"] = df_vacc.apply(
            lambda row: dt.fromisocalendar(row["År"], row["Vecka"], row["day"]), axis=1
        )

    # We need to calculate values for the population. Don't use the values for just the population eligible for vaccination
    df_vacc["Andel vaccinerade"] = df_vacc["Andel vaccinerade"].replace(
        ",", ".", regex=True
    )
    df_vacc["Procent vaccinerade"] = (df_vacc["Andel vaccinerade"].astype(float)) * 100

    # need to change 'Sverige' to 'Sweden'
    df_vacc = df_vacc.replace("| Sverige |", "Sweden")
    if only_sweden:
        df_vacc = df_vacc[df_vacc["Region"] == "Sweden"]

    # have only relevant column if needed
    if needed_columns:
        df_vacc = df_vacc[needed_columns]

    return df_vacc


data_url = "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data"

first_two_timeseries_lan = get_vaccination_data(
    data_url=data_url,
    sheet_name="Vaccinerade tidsserie",
    set_date=True,
    needed_columns=[
        "date",
        "Region",
        "Antal vaccinerade",
        "Procent vaccinerade",
        "Vaccinationsstatus",
    ],
)
first_two_timeseries = first_two_timeseries_lan[
    first_two_timeseries_lan["Region"] == "Sweden"
]

third_timseries_lan = get_vaccination_data(
    data_url=data_url,
    sheet_name="Vaccinerade tidsserie dos 3",
    set_date=True,
    # only_sweden=True,
    needed_columns=[
        "date",
        "Region",
        "Antal vaccinerade",
        "Procent vaccinerade",
        "Vaccinationsstatus",
    ],
)

third_timseries = third_timseries_lan[third_timseries_lan["Region"] == "Sweden"]

fourth_timseries_lan = get_vaccination_data(
    data_url=data_url,
    sheet_name="Vaccinerade tidsserie dos 4",
    set_date=True,
    # only_sweden=True,
    needed_columns=[
        "date",
        "Region",
        "Antal vaccinerade",
        "Procent vaccinerade",
        "Vaccinationsstatus",
    ],
)

fourth_timseries = fourth_timseries_lan[fourth_timseries_lan["Region"] == "Sweden"]

first_three_vacc_dose_lan = get_vaccination_data(
    data_url=data_url, sheet_name="Dos 1 till 3 per åldersgrupp"
)
first_three_vacc_dose = first_three_vacc_dose_lan[
    first_three_vacc_dose_lan["Region"] == "Sweden"
]

# third_vacc_dose_lan = get_vaccination_data(
#     data_url=data_url,
#     sheet_name="Dos 3 per åldersgrupp"
#     )
# third_vacc_dose = third_vacc_dose_lan[third_vacc_dose_lan["Region"] == "Sweden"]

fourth_vacc_dose_lan = get_vaccination_data(
    data_url=data_url, sheet_name="Dos 4 per åldersgrupp"
)
fourth_vacc_dose = fourth_vacc_dose_lan[fourth_vacc_dose_lan["Region"] == "Sweden"]

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
