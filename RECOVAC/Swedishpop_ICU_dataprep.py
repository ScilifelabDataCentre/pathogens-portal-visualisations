# This script prepares the data to be used in plots showing ICU coverage over time
# Data is given for different dose levels, and different age groups
# RECOVAC provides data
# Data given for 3 age ranges - 18+, 18-59, and 60+
# Data given for first 4 doses

import pandas as pd
from datetime import datetime as dt

RECO_icu_18plus = pd.read_excel(
    "data/iva_vacc_18plus.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_icu_18to59 = pd.read_excel(
    "data/iva_vacc_18-59.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_icu_60plus = pd.read_excel(
    "data/iva_vacc_60plus.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

def date_func(dataset):
    dataset[["Year", "Week"]] = (
        dataset["wk"].str.split("w", expand=True).astype(int)
    )  # break apart week and year
    dataset["day"] = 1  # set day as Monday
    dataset.drop(dataset[(dataset["Year"] == 2019)].index, inplace=True)
    dataset["date"] = dataset.apply(
        lambda row: dt.fromisocalendar(row["Year"], row["Week"], row["day"]), axis=1
    )
    pd.to_datetime(dataset["date"])
    dataset.drop(columns=["Week", "Year", "day", "wk"], axis=1, inplace=True)
    dataset["date"] = dataset["date"].astype(str)
    # print(dataset.head())


datasets = {
    "icu_18plus": RECO_icu_18plus,
    "icu_18to59": RECO_icu_18to59,
    "icu_60plus": RECO_icu_60plus,
}

for name, df in datasets.items():
    date_func(df)
