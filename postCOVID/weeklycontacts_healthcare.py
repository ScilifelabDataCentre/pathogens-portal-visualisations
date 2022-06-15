import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.express as px
import os
import argparse

aparser = argparse.ArgumentParser(description="Generate weekly contact blob")
aparser.add_argument("--output-dir", nargs="?", default="postcovid_plots",
                     help="Output directory where the files will be saved")
args = aparser.parse_args()

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

healthcare_contacts["Year"] = np.nan
healthcare_contacts.loc[:32, "Year"] = 2020
healthcare_contacts.loc[32:84, "Year"] = 2021
healthcare_contacts.loc[84:136, "Year"] = 2022
healthcare_contacts.loc[136:188, "Year"] = 2023
# if this is still being used in 2024, we will need to add (written week 2 of 2022)

# Need to drop last 3 rows because notes are included in the datafile.
# remove/edit if this changes in future, but without it, you get an error generating the date.
healthcare_contacts.drop(index=healthcare_contacts.index[-3:], axis=0, inplace=True)

healthcare_contacts["day"] = 1

# generate a 'real' date from week info
healthcare_contacts["date"] = healthcare_contacts.apply(
    lambda row: dt.fromisocalendar(
        int(row["Year"]), int(row["Vecka"]), int(row["day"])
    ),
    axis=1,
)

healthcare_contacts.rename(
    columns={"U08.9": "U089", "U09.9": "U099", "Z86.1A": "Z861A"}, inplace=True
)

healthcare_contacts = healthcare_contacts.replace(r"^\s*$", np.nan, regex=True)

fig = go.Figure(
    data=[
        go.Scatter(
            name="U08.9",
            x=healthcare_contacts.date,
            y=healthcare_contacts.U089,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[0], size=3),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[0], width=1),
        ),
        go.Scatter(
            name="U09.9",
            x=healthcare_contacts.date,
            y=healthcare_contacts.U099,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[8], size=3),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[8], width=1),
        ),
        go.Scatter(
            name="Z86.1A",
            x=healthcare_contacts.date,
            y=healthcare_contacts.Z861A,
            mode="lines+markers",
            marker=dict(color="gold", size=3),
            marker_symbol="square",
            line=dict(color="gold", width=1),
        ),
    ]
)
fig.update_layout(
    plot_bgcolor="white",
    autosize=False,
    font=dict(size=14),
    margin=dict(r=150, t=0, b=0, l=0),
    legend=dict(
        title="<b>Diagnosis</b>",
    ),
    hovermode="x unified",
    hoverdistance=1,
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
)
fig.update_yaxes(
    title="<b>Contacts with healthcare<br></b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    range=[0, (max(healthcare_contacts.U089) * 1.15)],
    rangemode="tozero",
)
#fig.show()
if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)
fig.write_json(os.path.join(args.output_dir, "weeklycontacts_healthcare.json"))
