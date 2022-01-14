import pandas as pd
import json

# Import and sort data
accom_diag = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - andra diagnoser",
    header=3,
    engine="openpyxl",
    keep_default_na=False,
)

accom_diag = accom_diag.iloc[0:13, 0:3]

accom_diag.columns = [
    "diagnoses_group",
    "number_of_patients",
    "percentage_of_patients",
]

accom_diag["percentage_of_patients"] = (
    accom_diag["percentage_of_patients"].astype(float).map("{:.0%}".format)
)

# make the structure such that each row

accom_diag = [
    {
        "diagnoses_group": "Lung function/Breathing",
        "number_of_patients": accom_diag.number_of_patients[0],
        "percentage_of_patients": accom_diag.percentage_of_patients[0],
    },
    {
        "diagnoses_group": "Brain fog/Cognitive impairment",
        "number_of_patients": accom_diag.number_of_patients[1],
        "percentage_of_patients": accom_diag.percentage_of_patients[1],
    },
    {
        "diagnoses_group": "Pain",
        "number_of_patients": accom_diag.number_of_patients[2],
        "percentage_of_patients": accom_diag.percentage_of_patients[2],
    },
    {
        "diagnoses_group": "Palpitations",
        "number_of_patients": accom_diag.number_of_patients[3],
        "percentage_of_patients": accom_diag.percentage_of_patients[3],
    },
    {
        "diagnoses_group": "COPD/Asthma",
        "number_of_patients": accom_diag.number_of_patients[4],
        "percentage_of_patients": accom_diag.percentage_of_patients[4],
    },
    {
        "diagnoses_group": "Pneumonia",
        "number_of_patients": accom_diag.number_of_patients[5],
        "percentage_of_patients": accom_diag.percentage_of_patients[5],
    },
    {
        "diagnoses_group": "Kidney issues",
        "number_of_patients": accom_diag.number_of_patients[6],
        "percentage_of_patients": accom_diag.percentage_of_patients[6],
    },
    {
        "diagnoses_group": "Smell/Taste",
        "number_of_patients": accom_diag.number_of_patients[7],
        "percentage_of_patients": accom_diag.percentage_of_patients[7],
    },
    {
        "diagnoses_group": "Neurological problems",
        "number_of_patients": accom_diag.number_of_patients[8],
        "percentage_of_patients": accom_diag.percentage_of_patients[8],
    },
    {
        "diagnoses_group": "Sleep disorder",
        "number_of_patients": accom_diag.number_of_patients[9],
        "percentage_of_patients": accom_diag.percentage_of_patients[9],
    },
    {
        "diagnoses_group": "Fever",
        "number_of_patients": accom_diag.number_of_patients[10],
        "percentage_of_patients": accom_diag.percentage_of_patients[10],
    },
    {
        "diagnoses_group": "Dizziness/Nausea",
        "number_of_patients": accom_diag.number_of_patients[11],
        "percentage_of_patients": accom_diag.percentage_of_patients[11],
    },
    {
        "diagnoses_group": "Depression/Anxiety",
        "number_of_patients": accom_diag.number_of_patients[12],
        "percentage_of_patients": accom_diag.percentage_of_patients[12],
    },
    #    for _, row in accom_diag_swe.iterrows()
]

jsonStr = json.dumps(accom_diag)

with open("accompanying_diagnoses.json", "w") as file:
    file.write(jsonStr)
