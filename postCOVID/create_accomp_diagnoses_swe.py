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

# print(accom_diag)

fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[13, 10, 10],
            header=dict(
                values=[
                    "<b>Diagnosgrupp (ICD-10-SE)</b>",
                    "<b>Antal patienter</b>",
                    "<b>Andel patienter</b>",
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
fig.write_json("accompdiag_table_swe.json")
