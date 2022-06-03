# This script prepares the data to be used in plots showing vaccination coverage over time
# Data is given for different dose levels, and different age groups
# RECOVAC provides data
# Data given for 3 age ranges - 18+, 18-59, and 60+
# Data given for first 4 doses
# Graph will be 'area under the curve'
import pandas as pd
from datetime import datetime as dt

# first load data.
# 18+ age
RECO_18plus = pd.read_excel(
    "data/vacc_pop_18plus_25 May 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# 18-59 age
RECO_18to59 = pd.read_excel(
    "data/vacc_pop_18-59_25 May 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# 60+ age
RECO_60plus = pd.read_excel(
    "data/vacc_pop_60plus_25 May 2022.xlsx",
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
    # print(dataset.head())


# Need to do some calculations to get JUST those with 1 dose, with 2 doses.. and calc. 0 doses
# In the original dataset e.g. one dose included anyone that had had a dose (so includes 2 dose, 3 dose..)
def calc_func(dataset):
    # need to work out proportions UNVACCINATED - sum rest and minus from 1
    dataset.replace(r"^\s*$", 0.0, regex=True, inplace=True)
    dataset["no_dose"] = (1 - dataset["vacc1"]) * 100
    dataset["one_dose"] = (dataset["vacc1"] - dataset["vacc2"]) * 100
    dataset["two_dose"] = (dataset["vacc2"] - dataset["vacc3"]) * 100
    dataset["three_dose"] = (dataset["vacc3"] - dataset["vacc4"]) * 100
    dataset["four_dose"] = dataset["vacc4"]
    dataset.drop(columns=["vacc1", "vacc2", "vacc3", "vacc4"], axis=1, inplace=True)
    # print(dataset.head())


# make a list of datasets on which to perform the function

datasets = [RECO_18plus, RECO_18to59, RECO_60plus]

# run the functions to recalculate the proportions and format the date
for x in datasets:
    date_func(x)

for y in datasets:
    calc_func(y)
