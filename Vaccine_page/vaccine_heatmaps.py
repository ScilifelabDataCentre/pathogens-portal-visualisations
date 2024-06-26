import argparse
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np  # won't need this when data on 3rd dose for 12-17 year olds becomes available
import os

from vaccine_dataprep_Swedentots import (
    first_three_vacc_dose,
    # third_vacc_dose_lan,
    fourth_vacc_dose,
    fifth_vacc_dose,
)

aparser = argparse.ArgumentParser(description="Generate text insert json")
aparser.add_argument(
    "--output-dir",
    nargs="?",
    default="vaccine_plots",
    help="Output directory where the files will be saved",
)
args = aparser.parse_args()

# Don't have population size data for these age groups (at least right now), so can't do population level calculations

## data on first 3 doses held together, 4th held seperately.

# Need to change terminology used for the '90 or older' age group
first_three_vacc_dose = first_three_vacc_dose.replace("90 eller äldre", "90+")

# We drop the 'totals' in the dataset as we don't want them
first_three_vacc_dose.drop(
    first_three_vacc_dose[(first_three_vacc_dose["Åldersgrupp"] == "Totalt 18+")].index,
    inplace=True,
)

# recaculate as a percentage for each age group.
first_three_vacc_dose["Procent vaccinerade"] = (
    first_three_vacc_dose["Andel vaccinerade"] * 100
)

# Separate data for one and two doses

# one dose
one_dose = first_three_vacc_dose[
    (first_three_vacc_dose["Vaccinationsstatus"] == "1 dos")
]
one_dose = one_dose[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
one_dose.reset_index(drop=True, inplace=True)

# data for two doses
two_doses = first_three_vacc_dose[
    (first_three_vacc_dose["Vaccinationsstatus"] == "2 doser")
]
two_doses = two_doses[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
two_doses.reset_index(drop=True, inplace=True)

## Sort data for three doses. Note - data only currently available for 18+ (from 12 for 1 & 2 dose)

# data for three doses
three_doses = first_three_vacc_dose[
    (first_three_vacc_dose["Vaccinationsstatus"] == "Minst 3 doser")
]
three_doses = three_doses[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
three_doses.reset_index(drop=True, inplace=True)

# For now, we need to add two age categories for the third dose (12-15, 16-17)
## REMOVE THIS ROW WHEN THESE AGE CATEGORIES ARE AVAILABLE FOR THIRD DOSE DATA
top_row = pd.DataFrame(
    {
        "Åldersgrupp": ["12-15", "16-17"],
        "Procent vaccinerade": [np.nan, np.nan],
        "Vaccinationsstatus": ["Minst 3 doser", "Minst 3 doser"],
    }
)
third_dose = pd.concat([top_row, three_doses]).reset_index(drop=True)

# Add fourth dose (already as percentages from dataprep, so not needed)
# For now, we need to add two age categories for the fourth dose (12-15, 16-17)
## REMOVE THIS ROW WHEN THESE AGE CATEGORIES ARE AVAILABLE FOR fourth DOSE DATA
# Also need to eliminate 'totalt' row
fourth_vacc_dose = fourth_vacc_dose.replace("90 eller äldre", "90+")
# REMOVE BELOW AS MORE AGE CATEGORIES ARE ADDED
top_row_fourth = pd.DataFrame(
    {
        "Åldersgrupp": [
            "12-15",
            "16-17",
        ],
        "Procent vaccinerade": [
            np.nan,
            np.nan,
        ],
        "Vaccinationsstatus": [
            "Minst 4 doser",
            "Minst 4 doser",
        ],
    }
)
fourth_dose = pd.concat([top_row_fourth, fourth_vacc_dose]).reset_index(drop=True)
fourth_dose = fourth_dose[fourth_dose.Åldersgrupp != "Totalt"]

# Add fifth dose (already as percentages from dataprep, so not needed)
# do need to add additional age group rows (until more are added amd change 90+ )
# Also need to eliminate 'totalt' row
fifth_vacc_dose = fifth_vacc_dose.replace("90 eller äldre", "90+")
# REMOVE BELOW AS MORE AGE CATEGORIES ARE ADDED
top_row_fifth = pd.DataFrame(
    {
        "Åldersgrupp": [
            "12-15",
            "16-17",
            "18-29",
            "30-39",
            "40-49",
            "50-59",
            "60-69",
        ],
        "Procent vaccinerade": [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
        "Vaccinationsstatus": [
            "5 doser",
            "5 doser",
            "5 doser",
            "5 doser",
            "5 doser",
            "5 doser",
            "5 doser",
        ],
    }
)
fifth_dose = pd.concat([top_row_fifth, fifth_vacc_dose]).reset_index(drop=True)
fifth_dose = fifth_dose[fifth_dose.Åldersgrupp != "Totalt"]
fifth_dose = fifth_dose[fifth_dose.Åldersgrupp != "65-69"]

## Prepare dataframe for heatmap (all data in one place)

heatmap_data = pd.concat(
    [one_dose, two_doses, third_dose, fourth_dose, fifth_dose],
    axis=0,
)
heatmap_data["Vaccinationsstatus"] = heatmap_data["Vaccinationsstatus"].replace(
    {
        "1 dos": "1",
        "2 doser": "2",
        "Minst 3 doser": "3",
        "Minst 4 doser": "4",
        "5 doser": "5",
    }
)

## Make heatmap figures (one small for front of portal, and one larger for page)
## Same data will be included in both

colours = px.colors.diverging.RdBu

fig_small = go.Figure(
    data=go.Heatmap(
        z=heatmap_data["Procent vaccinerade"],
        zmin=0,
        zmax=100,
        x=heatmap_data["Vaccinationsstatus"],
        y=heatmap_data["Åldersgrupp"],
        xgap=1,
        ygap=1,
        colorbar={
            "title": "<b>Percentage of <br>Population Vaccinated<br> </b>",
            "yanchor": "top",
            "y": 1.0,
            "lenmode": "fraction",
            "len": 0.95,
            "tickvals": [
                5,
                15,
                25,
                35,
                45,
                55,
                65,
                75,
                85,
                95,
            ],
            "ticktext": [
                "00.00-9.99%",
                "10.00-19.99%",
                "20.00-29.99%",
                "30.00-39.99%",
                "40.00-49.99%",
                "50.00-59.99%",
                "60.00-69.99%",
                "70.00-79.99%",
                "80.00-89.99%",
                "90.00-100.00%",
            ],
        },
        colorscale=[
            [0.0, colours[10]],
            [0.1, colours[10]],
            [0.1, colours[9]],
            [0.2, colours[9]],
            [0.2, colours[8]],
            [0.3, colours[8]],
            [0.3, colours[7]],
            [0.4, colours[7]],
            [0.4, colours[6]],
            [0.5, colours[6]],
            [0.5, "rgb(255,255,204)"],
            [0.6, "rgb(255,255,204)"],
            [0.6, colours[4]],
            [0.7, colours[4]],
            [0.7, colours[3]],
            [0.8, colours[3]],
            [0.8, colours[2]],
            [0.9, colours[2]],
            [0.9, colours[1]],
            [1.0, colours[1]],
        ],
        hovertemplate="<extra></extra>Vaccine Doses Received: %{x} <br>Age Category: %{y}<br>Percentage Vaccinated: %{z:.2f}%",
    )
)
fig_small.update_layout(
    hoverlabel={
        "bgcolor": "white",
        "font_size": 12,
    }
)
fig_small.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig_small.update_layout(
    title=" ",
    plot_bgcolor="white",
    # autosize=False,
    yaxis={
        "title": "<b>Age Group</b>",
        "linecolor": "black",
    },
    font={"size": 12},
    # width=2000, # Don't set width/height, it's set in Portal
    # height=300,  # It's the legend length and font that make this heatmap 'small'
    xaxis={
        "title": "<b>Doses Received</b>",
        "tickangle": 0,
        "zeroline": True,
        "linecolor": "black",
    },
)

# fig_small.show()
if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)

fig_small.write_json(os.path.join(args.output_dir, "vaccine_heatmap_small.json"))
# fig_small.write_image("Plots/vaccine_heatmap_small.png")

# Now make the larger version

fig = go.Figure(
    data=go.Heatmap(
        z=heatmap_data["Procent vaccinerade"],
        zmin=0,
        zmax=100,
        x=heatmap_data["Vaccinationsstatus"],
        y=heatmap_data["Åldersgrupp"],
        xgap=1,
        ygap=1,
        colorbar={
            "title": "<b>Percentage of <br>Population Vaccinated<br> </b>",
            "yanchor": "top",
            "y": 1.0,
            "lenmode": "fraction",
            "len": 0.5,
            "tickvals": [
                5,
                15,
                25,
                35,
                45,
                55,
                65,
                75,
                85,
                95,
            ],
            "ticktext": [
                "00.00-9.99%",
                "10.00-19.99%",
                "20.00-29.99%",
                "30.00-39.99%",
                "40.00-49.99%",
                "50.00-59.99%",
                "60.00-69.99%",
                "70.00-79.99%",
                "80.00-89.99%",
                "90.00-100.00%",
            ],
        },
        colorscale=[
            [0.0, colours[10]],
            [0.1, colours[10]],
            [0.1, colours[9]],
            [0.2, colours[9]],
            [0.2, colours[8]],
            [0.3, colours[8]],
            [0.3, colours[7]],
            [0.4, colours[7]],
            [0.4, colours[6]],
            [0.5, colours[6]],
            [0.5, "rgb(255,255,204)"],
            [0.6, "rgb(255,255,204)"],
            [0.6, colours[4]],
            [0.7, colours[4]],
            [0.7, colours[3]],
            [0.8, colours[3]],
            [0.8, colours[2]],
            [0.9, colours[2]],
            [0.9, colours[1]],
            [1.0, colours[1]],
        ],
        hovertemplate="<extra></extra>Vaccine Doses Received: %{x} <br>Age Category: %{y}<br>Percentage Vaccinated: %{z:.2f}%",
    )
)
fig.update_layout(
    hoverlabel={
        "bgcolor": "white",
        "font_size": 14,
    }
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(
    title=" ",
    plot_bgcolor="white",
    # autosize=False,
    yaxis={
        "title": "<b>Age Group</b>",
        "linecolor": "black",
    },
    font={"size": 14},
    # width=2000, # width/height not set - will depend on portal space
    # height=1000,  # it's the legend length and font etc. that make this 'larger'
    xaxis={
        "title": "<b>Doses Received</b>",
        "tickangle": 0,
        "zeroline": True,
        "linecolor": "black",
    },
)

fig.write_json(os.path.join(args.output_dir, "vaccine_heatmap.json"))
# fig.write_image("Plots/vaccine_heatmap.png")

# # fig.show()
