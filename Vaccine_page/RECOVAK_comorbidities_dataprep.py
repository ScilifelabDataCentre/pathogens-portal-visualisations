# script looks at cormorbitities data (cancer, diabetes, cardio issues, and respiratory diseases)
# Data considers cases vs vaccination doses for people with these comorbidities
import pandas as pd
from datetime import datetime as dt

# Import data

RECO_cancer = pd.read_excel(
    "data/SciLifeLab Collab_comorb_cancer_vacc.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_cardio = pd.read_excel(
    "data/SciLifeLab Collab_comorb_cvd_cardio_vacc.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_diabetes = pd.read_excel(
    "data/SciLifeLab Collab_comorb_dm_vacc.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_resp = pd.read_excel(
    "data/SciLifeLab Collab_comorb_resp_dis1_vacc.xlsx",
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
    dataset.drop(
        columns=["Week", "Year", "day", "wk"], axis=1, inplace=True
    )  # [["date", "c19_d2", "vacc0", "vacc1", "vacc2", "vacc3"]]
    # print(dataset.head())


# make a list of datasets and add function to run function

datasets = [RECO_cancer, RECO_cardio, RECO_diabetes, RECO_resp]

for x in datasets:
    date_func(x)
