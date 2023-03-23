# script looks at cormorbitities data (cancer, diabetes, cardio issues, and respiratory diseases)
# Data considers cases vs vaccination doses for people with these comorbidities
import pandas as pd
from datetime import datetime as dt

# Import data

RECO_cancer = pd.read_excel(
    "data/cm_sos_cancer_covid_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_cardio = pd.read_excel(
    "data/cm_cvd_cardio_covid_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_diabetes = pd.read_excel(
    "data/cm_dm_covid_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_resp = pd.read_excel(
    "data/cm_resp_dis1_covid_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

## Set date on dataframes


def date_func(dataset):
    dataset[["Year", "Week"]] = (
        dataset["wk"].str.split("w", expand=True).astype(int)
    )  # break apart week and year
    dataset["day"] = 1  # set day as Monday
    dataset.drop(dataset[(dataset["Year"] == 2019)].index, inplace=True)
    dataset["date"] = dataset.apply(
        lambda row: dt.fromisocalendar(row["Year"], row["Week"], row["day"]), axis=1
    )
    dataset.drop(dataset[(dataset["date"] < "2020-01-31")].index, inplace=True)
    dataset.drop(columns=["Week", "Year", "day", "wk"], axis=1, inplace=True)
    # print(dataset.head())


# make a list of datasets and add function to run function

datasets = [RECO_cancer, RECO_cardio, RECO_diabetes, RECO_resp]

for x in datasets:
    date_func(x)
