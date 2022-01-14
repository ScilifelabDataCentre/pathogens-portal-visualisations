import pandas as pd
import json

# Import and sort data
healthcare_contacts_week_sex = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - kön vecka",
    header=6,
    engine="openpyxl",
    keep_default_na=False,
)

healthcare_contacts_week_sex = healthcare_contacts_week_sex.replace(
    {
        "v1": "1",
        "v2": "2",
        "v3": "3",
        "v4": "4",
        "v5": "5",
        "v6": "6",
        "v7": "7",
        "v8": "8",
        "v9": "9",
        "X": "",
        "2020 ": "",
        "2021 ": "",
        "2022 ": "",
        "2023 ": "",
    },
    regex=True,
)

# if this is still being used in 2024, we will need to add (written week 2 of 2022)

# two dataframes given on tab. Probably easiest to deal with both seperately (also 2 timeframes).

# trim rows/columns for the two diagnoses
U099 = healthcare_contacts_week_sex.iloc[:, 0:3]
U089 = healthcare_contacts_week_sex.iloc[:, 5:8]

U099.columns = [
    "Vecka",
    "Male",
    "Female",
]
U089.columns = [
    "Vecka",
    "Male",
    "Female",
]

# set years to appropriate rows (according to timeframes)
U089["Year"] = ""
U089["Year"][:32] = 2020
U089["Year"][32:84] = 2021
U089["Year"][84:136] = 2022
U089["Year"][136:188] = 2023

U099["Year"] = ""
U099["Year"][:11] = 2020
U099["Year"][11:63] = 2021
U099["Year"][63:115] = 2022
U099["Year"][115:167] = 2023

# if this is still being used in 2024, we will need to add (written week 2 of 2022)

# drop blank space at the bottoms of dataframes (including the additional notes placed there)
U099.drop(index=U099.index[-25:], axis=0, inplace=True)
U089.drop(index=U089.index[-4:], axis=0, inplace=True)

# get date in appropriate format
U089["week"] = U089["Year"].astype(str) + "-" + U089["Vecka"].astype(str)

U099["week"] = U099["Year"].astype(str) + "-" + U099["Vecka"].astype(str)

U089 = U089.replace(
    {
        "2021-1": "2021-01",
        "2021-2": "2021-02",
        "2021-3": "2021-03",
        "2021-4": "2021-04",
        "2021-5": "2021-05",
        "2021-6": "2021-06",
        "2021-7": "2021-07",
        "2021-8": "2021-08",
        "2021-9": "2021-09",
        "2022-1": "2022-01",
        "2022-2": "2022-02",
        "2022-3": "2022-03",
        "2022-4": "2022-04",
        "2022-5": "2022-05",
        "2022-6": "2022-06",
        "2022-7": "2022-07",
        "2022-8": "2022-08",
        "2022-9": "2022-09",
        "2023-1": "2023-01",
        "2023-2": "2023-02",
        "2023-3": "2023-03",
        "2023-4": "2023-04",
        "2023-5": "2023-05",
        "2023-6": "2023-06",
        "2023-7": "2023-07",
        "2023-8": "2023-08",
        "2023-9": "2023-09",
    },
    #    regex=True,
)

U099 = U099.replace(
    {
        "2021-1": "2021-01",
        "2021-2": "2021-02",
        "2021-3": "2021-03",
        "2021-4": "2021-04",
        "2021-5": "2021-05",
        "2021-6": "2021-06",
        "2021-7": "2021-07",
        "2021-8": "2021-08",
        "2021-9": "2021-09",
        "2022-1": "2022-01",
        "2022-2": "2022-02",
        "2022-3": "2022-03",
        "2022-4": "2022-04",
        "2022-5": "2022-05",
        "2022-6": "2022-06",
        "2022-7": "2022-07",
        "2022-8": "2022-08",
        "2022-9": "2022-09",
        "2023-1": "2023-01",
        "2023-2": "2023-02",
        "2023-3": "2023-03",
        "2023-4": "2023-04",
        "2023-5": "2023-05",
        "2023-6": "2023-06",
        "2023-7": "2023-07",
        "2023-8": "2023-08",
        "2023-9": "2023-09",
    },
    #    regex=True,
)

# Add diagnosis codes to each dataset

U099["diagnosis"] = "u09_9"
U089["diagnosis"] = "u08_9"
U099["sex_f"] = "female"
U089["sex_f"] = "female"
U099["sex_m"] = "male"
U089["sex_m"] = "male"

# Think quickest way to get the format required for datagraphics plots is to split up by sex AND diagnosis

U099_male_data = [U099["week"], U099["diagnosis"], U099["Male"], U099["sex_m"]]
U099_female_data = [U099["week"], U099["diagnosis"], U099["Female"], U099["sex_f"]]

U089_male_data = [U089["week"], U089["diagnosis"], U089["Male"], U089["sex_m"]]
U089_female_data = [U089["week"], U089["diagnosis"], U089["Female"], U089["sex_f"]]

U099_male_header = ["week", "diagnosis", "number_healthcare_contacts", "sex"]
U099_female_header = ["week", "diagnosis", "number_healthcare_contacts", "sex"]
U089_male_header = ["week", "diagnosis", "number_healthcare_contacts", "sex"]
U089_female_header = ["week", "diagnosis", "number_healthcare_contacts", "sex"]

U099_male_df = pd.concat(U099_male_data, axis=1, keys=U099_male_header)
U099_female_df = pd.concat(U099_female_data, axis=1, keys=U099_female_header)
U089_male_df = pd.concat(U089_male_data, axis=1, keys=U089_male_header)
U089_female_df = pd.concat(U089_female_data, axis=1, keys=U089_female_header)

formatted_df_weeklycontacts_sexdiag = pd.concat(
    [U099_male_df, U099_female_df, U089_male_df, U089_female_df], ignore_index=True
)

# print(formatted_df_weeklycontacts_sexdiag)

formatted_df_weeklycontacts_sexdiag.to_csv(
    "contacts_healthcare_divby_week_sex.csv", index=False
)

# load this on to: https://datagraphics.dckube.scilifelab.se/dataset/c5b6ab32536649a59781a92f8ac932f3
