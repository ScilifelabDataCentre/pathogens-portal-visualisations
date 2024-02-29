# Data preparation FOR PLOTS BASED ON VACCINATION RATE FOR COMORBIDITY GROUPS!
import pandas as pd
from datetime import datetime as dt

# load vaccine data time series for vaccine coverage

# cardiovascular disease
RECO_cvd_V = pd.read_excel(
    "data/cm_cvd_cardio_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# diabetes
RECO_dm_V = pd.read_excel(
    "data/cm_dm_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# respiratory disease
RECO_resp_V = pd.read_excel(
    "data/cm_resp_dis1_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# cancer
RECO_cancer_V = pd.read_excel(
    "data/cm_sos_cancer_vacc_SciLifeLab.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# function to change the date:
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
    # print(dataset.info())


# Need to do some calculations to get JUST those with 1 dose, with 2 doses.. and calc. 0 doses
# In the original dataset e.g. one dose included anyone that had had a dose (so includes 2 dose, 3 dose..)
def calc_func(dataset):
    # need to work out proportions UNVACCINATED - sum rest and minus from 1
    dataset.replace(r"^\s*$", 0.0, regex=True, inplace=True)
    dataset.set_axis(
        ["vacc1", "vacc2", "vacc3", "vacc4", "vacc5", "vacc6", "date"],
        axis=1,
        inplace=True,
    )
    dataset["no_dose"] = (1 - dataset["vacc1"]) * 100
    dataset["one_dose"] = (dataset["vacc1"] - dataset["vacc2"]) * 100
    dataset["two_dose"] = (dataset["vacc2"] - dataset["vacc3"]) * 100
    dataset["three_dose"] = (dataset["vacc3"] - dataset["vacc4"]) * 100
    dataset["four_dose"] = (dataset["vacc4"] - dataset["vacc5"]) * 100
    dataset["five_dose"] = (dataset["vacc5"] - dataset["vacc6"]) * 100
    dataset["six_dose"] = dataset["vacc6"] * 100
    # will need to modify and expand this as more doses are added
    dataset.drop(
        columns=["vacc1", "vacc2", "vacc3", "vacc4", "vacc5", "vacc6"],
        axis=1,
        inplace=True,
    )
    cols = [
        "no_dose",
        "one_dose",
        "two_dose",
        "three_dose",
        "four_dose",
        "five_dose",
        "six_dose",
    ]
    dataset[cols] = dataset[cols].ffill()


# make a list of datasets on which to perform the function

datasets = [RECO_cvd_V, RECO_dm_V, RECO_resp_V, RECO_cancer_V]

# run the functions to recalculate the proportions and format the date
for x in datasets:
    date_func(x)

for y in datasets:
    calc_func(y)
