import pandas as pd
import json
import plotly.graph_objects as go

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

# Need to setup conversions to Swedish.
# Think it is best to set up conversions, rather than set 'hard values' in a column
# Logic: if the order changes, it'll be wrong.
# Note: If they change the words used for diagnosis, we will need to change this part of the script accordingly
# Make a dictionary for the changes - easy to modify later

dic = {
    "Lungfunktion/Andning": "Lung function/Breathing",
    "Hjärntrötthet/Kognitiv nedsättning": "Brain fog/Cognitive impairment",
    "Smärta": "Pain",
    "Hjärtklappning/POTS": "Palpitations",
    "Kol/Astma": "COPD/Asthma",
    "Pneumoni": "Pneumonia",
    "Njurbesvär": "Kidney issues",
    "Lukt/Smak": "Smell/Taste",
    "Neurologiska besvär": "Neurological problems",
    "Sömnproblem": "Sleep disorder",
    "Feber": "Fever",
    "Yrsel/Illamående": "Dizziness/Nausea",
    "Depression/Ångest": "Depression/Anxiety",
}

accom_diag["diagnoses_group"] = accom_diag["diagnoses_group"].replace(dic, regex=True)

fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[13, 10, 10],
            header=dict(
                values=[
                    "<b>Diagnosis group (ICD-10-SE)</b>",
                    "<b>Number of patients</b>",
                    "<b>Percentage of patients</b>",
                ],
                align=["left"],
                fill_color="#ededed",
                font=dict(color="black", size=14),
                height=35,
                line=dict(color="#e0e0e0", width=0.05),
            ),
            cells=dict(
                values=(
                    accom_diag["diagnoses_group"],
                    accom_diag["number_of_patients"],
                    accom_diag["percentage_of_patients"],
                ),
                align=["left"],
                fill_color=["white"],
                font=dict(color="black", size=14),
                height=35,
                line=dict(color="#e0e0e0", width=0.05),
            ),
        )
    ]
)
fig.update_layout(margin={"r": 5, "t": 5, "l": 0, "b": 0})
fig.write_json("accompdiag_table.json")
