import pandas as pd
import json

# Import and sort data
age_sex_summ = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - ålder kön",
    header=10,
    engine="openpyxl",
    keep_default_na=False,
)

# trim rows/columns for the two diagnoses
U099 = age_sex_summ.iloc[0:3, 0:7]
U089 = age_sex_summ.iloc[12:15, 0:7]

# concat required values into a column

U099 = U099[["Unnamed: 1", "Unnamed: 3", "Unnamed: 5"]]
U089 = U089[["Unnamed: 1", "Unnamed: 3", "Unnamed: 5"]]

# initiate new dataframe

df = pd.DataFrame(columns=["diagnosis_code", "number_of_patients", "age_group", "sex"])

df["number_of_patients"] = (
    U099["Unnamed: 3"]
    .append(
        [
            U099["Unnamed: 5"],
            U099["Unnamed: 1"],
            U089["Unnamed: 3"],
            U089["Unnamed: 5"],
            U089["Unnamed: 1"],
        ]
    )
    .reset_index(drop=True)
)

df["diagnosis_code"] = [
    "U09.9",
    "U09.9",
    "U09.9",
    "U09.9",
    "U09.9",
    "U09.9",
    "U09.9",
    "U09.9",
    "U09.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
    "Z86.1A/U08.9",
]

df["age_group"] = [
    "0-17",
    "18-69",
    "70",
    "0-17",
    "18-69",
    "70",
    "0-17",
    "18-69",
    "70",
    "0-17",
    "18-69",
    "70",
    "0-17",
    "18-69",
    "70",
    "0-17",
    "18-69",
    "70",
]

df["sex"] = [
    "male",
    "male",
    "male",
    "female",
    "female",
    "female",
    "all",
    "all",
    "all",
    "male",
    "male",
    "male",
    "female",
    "female",
    "female",
    "all",
    "all",
    "all",
]

df.to_csv("summ_sex_age_bardata.csv")

# you should upload this to https://datagraphics.dckube.scilifelab.se/dataset/6b24d7130bef4bf78f567d9c9ad96f59
