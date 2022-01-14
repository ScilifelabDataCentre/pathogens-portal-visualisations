import pandas as pd
import json

# Import and sort data
healthcare_contacts = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - diagnoser över tid",
    header=4,
    engine="openpyxl",
    keep_default_na=False,
)

healthcare_contacts = healthcare_contacts.replace(
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

healthcare_contacts["Year"] = ""
healthcare_contacts["Year"][:32] = 2020
healthcare_contacts["Year"][32:84] = 2021
healthcare_contacts["Year"][84:136] = 2022
healthcare_contacts["Year"][136:188] = 2023
# if this is still being used in 2024, we will need to add (written week 2 of 2022)

healthcare_contacts.drop(index=healthcare_contacts.index[-3:], axis=0, inplace=True)

healthcare_contacts["week"] = (
    healthcare_contacts["Year"].astype(str)
    + "-"
    + healthcare_contacts["Vecka"].astype(str)
)

# Think that it's easiest to seperate the diagnoses to get format required for datagraphic plts (not python)

Z861A_data = [healthcare_contacts["week"], healthcare_contacts["Z86.1A"]]
U099_data = [healthcare_contacts["week"], healthcare_contacts["U09.9"]]
U089_data = [healthcare_contacts["week"], healthcare_contacts["U08.9"]]

Z861A_headers = ["week", "number_healthcare_contacts"]
U099_headers = ["week", "number_healthcare_contacts"]
U089_headers = ["week", "number_healthcare_contacts"]

Z861A = pd.concat(Z861A_data, axis=1, keys=Z861A_headers)
U099 = pd.concat(U099_data, axis=1, keys=U099_headers)
U089 = pd.concat(U089_data, axis=1, keys=U089_headers)

Z861A["diagnosis_code"] = "Z86.1A"
U099["diagnosis_code"] = "U09.9"
U089["diagnosis_code"] = "U08.9"

formatted_df_weeklycontacts = pd.concat([Z861A, U089, U099], ignore_index=True)

formatted_df_weeklycontacts = formatted_df_weeklycontacts.replace(
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

formatted_df_weeklycontacts.to_csv("contacts_healthcare_divby_week.csv", index=False)

# load this on to: https://datagraphics.dckube.scilifelab.se/dataset/2839da544c424e25916bf43eaa6c6210
