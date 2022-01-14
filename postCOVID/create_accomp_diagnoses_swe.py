import pandas as pd
import json

# Import and sort data
accom_diag_swe = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - andra diagnoser",
    header=3,
    engine="openpyxl",
    keep_default_na=False,
)

accom_diag_swe = accom_diag_swe.iloc[0:13, 0:3]

accom_diag_swe.columns = [
    "diagnoses_group",
    "number_of_patients",
    "percentage_of_patients",
]

accom_diag_swe["percentage_of_patients"] = (
    accom_diag_swe["percentage_of_patients"].astype(float).map("{:.0%}".format)
)

# make the structure such that each row

accom_diag_swe = [
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[0],
        "number_of_patients": accom_diag_swe.number_of_patients[0],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[0],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[1],
        "number_of_patients": accom_diag_swe.number_of_patients[1],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[1],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[2],
        "number_of_patients": accom_diag_swe.number_of_patients[2],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[2],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[3],
        "number_of_patients": accom_diag_swe.number_of_patients[3],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[3],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[4],
        "number_of_patients": accom_diag_swe.number_of_patients[4],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[4],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[5],
        "number_of_patients": accom_diag_swe.number_of_patients[5],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[5],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[6],
        "number_of_patients": accom_diag_swe.number_of_patients[6],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[6],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[7],
        "number_of_patients": accom_diag_swe.number_of_patients[7],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[7],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[8],
        "number_of_patients": accom_diag_swe.number_of_patients[8],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[8],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[9],
        "number_of_patients": accom_diag_swe.number_of_patients[9],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[9],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[10],
        "number_of_patients": accom_diag_swe.number_of_patients[10],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[10],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[11],
        "number_of_patients": accom_diag_swe.number_of_patients[11],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[11],
    },
    {
        "diagnoses_group": accom_diag_swe.diagnoses_group[12],
        "number_of_patients": accom_diag_swe.number_of_patients[12],
        "percentage_of_patients": accom_diag_swe.percentage_of_patients[12],
    },
    #    for _, row in accom_diag_swe.iterrows()
]

jsonStr = json.dumps(accom_diag_swe)

with open("accompanying_diagnoses_swe.json", "w") as file:
    file.write(jsonStr)
