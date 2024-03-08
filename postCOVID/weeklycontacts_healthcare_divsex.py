import pandas as pd
import numpy as np
import json
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.express as px
import os
import argparse

aparser = argparse.ArgumentParser(description="Generate weekly contact divsex blob")
aparser.add_argument(
    "--output-dir",
    nargs="?",
    default="postcovid_plots",
    help="Output directory where the files will be saved",
)
args = aparser.parse_args()

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
        "2023": "",  # added to account for a missing space in one of the data point labels
        "2024 ": "",
        "2024": "",
    },
    regex=True,
)

# if this is still being used in 2025, we will need to add (written week 8 of 2024)
# two dataframes given on tab. Easiest to deal with both seperately (also 2 timeframes).

# trim rows/columns for the two diagnoses
U099 = healthcare_contacts_week_sex.iloc[:, 0:3]
U089 = healthcare_contacts_week_sex.iloc[:, 5:8]

columns = [
    "Vecka",
    "Male",
    "Female",
]

U099.columns = columns
U089.columns = columns

# set years to appropriate rows (according to timeframes)
U089["Year"] = np.nan
U089.loc[:32, "Year"] = 2020
U089.loc[32:84, "Year"] = 2021
U089.loc[84:136, "Year"] = 2022
U089.loc[136:188, "Year"] = 2023
U089.loc[188:240, "Year"] = 2024

U099["Year"] = np.nan
U099.loc[:11, "Year"] = 2020
U099.loc[11:63, "Year"] = 2021
U099.loc[63:115, "Year"] = 2022
U099.loc[115:167, "Year"] = 2023
U099.loc[167:219, "Year"] = 2024

# if this is still being used in 2024, we will need to add (written week 2 of 2022)

# drop blank space at the bottoms of dataframes (including the additional notes placed there)
U099.drop(index=U099.index[-25:], axis=0, inplace=True)
U089.drop(index=U089.index[-4:], axis=0, inplace=True)

# Get dates in appropriate formats


def date_func(dataset):
    dataset["day"] = 1  # set day as Monday
    dataset["date"] = dataset.apply(
        lambda row: dt.fromisocalendar(
            int(row["Year"]), int(row["Vecka"]), int(row["day"])
        ),
        axis=1,
    )


datasets = [U089, U099]

for x in datasets:
    date_func(x)

# print(U089)
# print(U099)


def plot_healthcare_divsex(input, name):
    diagnosis = input
    fig = go.Figure(
        data=[
            go.Scatter(
                name="Female",
                x=diagnosis.date,
                y=diagnosis.Female,
                mode="lines+markers",
                marker=dict(color=px.colors.diverging.RdBu[0], size=3),
                marker_symbol="square",
                line=dict(color=px.colors.diverging.RdBu[0], width=1),
            ),
            go.Scatter(
                name="Male",
                x=diagnosis.date,
                y=diagnosis.Male,
                mode="lines+markers",
                marker=dict(color=px.colors.diverging.RdBu[8], size=3),
                marker_symbol="square",
                line=dict(color=px.colors.diverging.RdBu[8], width=1),
            ),
        ]
    )
    fig.update_layout(
        plot_bgcolor="white",
        # autosize=False,
        font=dict(size=12),
        margin=dict(r=0, t=50, b=0, l=0),
        legend=dict(
            orientation="h",
            # title="<b>Sex:</b>",
            yanchor="bottom",
            y=1,
            xanchor="left",
            x=-0.1,
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
        range=[0, (max(diagnosis.Female) * 1.15)],  # more female diagnosed
        rangemode="tozero",
    )
    # fig.show()
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    fig.write_json(
        os.path.join(args.output_dir, "{}_healthcare_divsex.json".format(name))
    )


plot_healthcare_divsex(U089, "U089")
plot_healthcare_divsex(U099, "U099")
