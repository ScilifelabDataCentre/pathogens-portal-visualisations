import pandas as pd
from datetime import datetime as dt

# Read the data
strain_data = pd.read_csv("data/Uppsala_data_2024-08-29_Nextclade.csv", sep=",")

# Express date as Year and Week for grouping
strain_data["date"] = pd.to_datetime(strain_data["date"])
strain_data["Year-Week"] = strain_data["date"].dt.strftime("%Y-%W")
strain_data["Year-Week"] = strain_data["Year-Week"].apply(lambda x: x.replace("2023-00", "2022-52"))

# Filter data from a specific date
strain_data = strain_data[(strain_data["date"] > "2023-10-01")]

# Calculate number of samples per week
number_samples_weekly = strain_data.groupby(["Year-Week"]).size().reset_index(name="strains_weekly")

# Calculate the number of each strain in each week
group_lineage_five = strain_data.groupby(["Year-Week", "lineage_groups05"]).size().reset_index(name="no_lineage5")

# Merge data and calculate percentages
lineage5_perc = pd.merge(group_lineage_five, number_samples_weekly, how="left", on="Year-Week")
lineage5_perc["percentage"] = (lineage5_perc["no_lineage5"] / lineage5_perc["strains_weekly"]) * 100

# Format dates for later use
lineage5_perc["year"] = lineage5_perc["Year-Week"].str[:4].astype(int)
lineage5_perc["week_no"] = lineage5_perc["Year-Week"].str[-3:].str.replace("-", "").astype(int)
lineage5_perc["day"] = 1
lineage5_perc["date"] = lineage5_perc.apply(lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1)


# 
def condition(x):
    if x == "BA.2":
        return 1
    elif x == "DV.7.1*":
        return 2
    elif x == "CH.*":
        return 3
    elif x == "BA.2.75* Other":
        return 4
    elif x == "JN.1*":
        return 5
    elif x == "JN.2*":
        return 6
    elif x == "JN.3*":
        return 7
    elif x == "BA.2.86* Other":
        return 8
    elif x == "BQ.*":
        return 9
    elif x == "JD.*":
        return 10
    elif x == "XBB.1.5* Other":
        return 11
    elif x == "FL.*":
        return 12
    elif x == "HK.*":
        return 13
    elif x == "JG.*":
        return 14
    elif x == "HV.*":
        return 15
    elif x == "EG.5.1* Other":
        return 16
    elif x == "EG.5* Other":
        return 17
    elif x == "XBB.1.9.2* Other":
        return 18
    elif x == "FU.*":
        return 19
    elif x == "XBB.1.16* Other":
        return 20
    elif x == "FY.*":
        return 21
    elif x == "XBB.2.3*":
        return 22
    elif x == "XBB* Other":
        return 23
    elif x == "XDA":
        return 24
    elif x == "XDD":
        return 25
    else:
        return 26


lineage5_perc["sort_lineages"] = lineage5_perc["lineage_groups05"].apply(condition)

# NB: an wrror may be thrown if the lineage is not in the dictionary.
lineage5_perc.sort_values(by=["sort_lineages"], inplace=True)
# print(lineage5_perc)


# Save the processed data to a CSV file
lineage5_perc.to_csv("data/weekly_data1.csv", index=False)
