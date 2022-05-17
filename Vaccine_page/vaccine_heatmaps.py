import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np  # won't need this when data on 3rd dose for 12-17 year olds becomes available
import os

from vaccine_dataprep_Swedentots import (
    first_two_vacc_dose_lan,
    third_vacc_dose_lan,
    fourth_vacc_dose,
)

## Need 3 sets of data - for one dose, two doses, and three doses
# Don't have population size data for these age groups (at least right now), so can't do population level calculations

## data for 3rd dose is held separately - work with data for 1st 2 doses first

first_two_vacc_dose_lan = first_two_vacc_dose_lan[(first_two_vacc_dose_lan["Region"] == "Sweden")]

# Need to change terminology used for the '90 or older' age group
first_two_vacc_dose_lan = first_two_vacc_dose_lan.replace("90 eller äldre", "90+")

# We drop the 'totals' in the dataset as we don't want them
first_two_vacc_dose_lan.drop(
    first_two_vacc_dose_lan[(first_two_vacc_dose_lan["Åldersgrupp"] == "Totalt")].index,
    inplace=True,
)

# recaculate as a percentage for each age group.
first_two_vacc_dose_lan["Procent vaccinerade"] = (
    first_two_vacc_dose_lan["Andel vaccinerade"] * 100
)

# Separate data for one and two doses

# one dose
one_dose = first_two_vacc_dose_lan[
    (first_two_vacc_dose_lan["Vaccinationsstatus"] == "Minst 1 dos")
]
one_dose = one_dose[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
one_dose.reset_index(drop=True, inplace=True)

# data for two doses
two_doses = first_two_vacc_dose_lan[
    (first_two_vacc_dose_lan["Vaccinationsstatus"] == "Minst 2 doser")
]
two_doses = two_doses[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
two_doses.reset_index(drop=True, inplace=True)

## Sort data for three doses. Note - data only currently available for 18+ (from 12 for 1 & 2 dose)

# Limit data to just Sweden and modify for the 90+ age group
third_vacc_dose_lan = third_vacc_dose_lan[(third_vacc_dose_lan["Region"] == "Sweden")]
third_vacc_dose_lan = third_vacc_dose_lan.replace("90 eller äldre", "90+")

# Calculate values as percentages
third_vacc_dose_lan.drop(
    third_vacc_dose_lan[(third_vacc_dose_lan["Åldersgrupp"] == "Totalt")].index,
    inplace=True,
)
third_vacc_dose_lan["Procent vaccinerade"] = (
    third_vacc_dose_lan["Andel vaccinerade"] * 100
)
third_vacc_dose_lan = third_vacc_dose_lan[
    ["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]
]

# For now, we need to add two age categories for the third dose (12-15, 16-17)
## REMOVE THIS ROW WHEN THESE AGE CATEGORIES ARE AVAILABLE FOR THIRD DOSE DATA
top_row = pd.DataFrame(
    {
        "Åldersgrupp": ["12-15", "16-17"],
        "Procent vaccinerade": [np.nan, np.nan],
        "Vaccinationsstatus": ["3 doser", "3 doser"],
    }
)
third_dose = pd.concat([top_row, third_vacc_dose_lan]).reset_index(drop=True)

# Add fourth dose (already as percentages from dataprep, so not needed)
# do need to add additional age group rows (until more are added amd change 90+ )
# Also need to eliminate 'totalt' row
fourth_vacc_dose = fourth_vacc_dose.replace("90 eller äldre", "90+")
# REMOVE BELOW AS MORE AGE CATEGORIES ARE ADDED
top_row_fourth = pd.DataFrame(
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
            "4 doser",
            "4 doser",
            "4 doser",
            "4 doser",
            "4 doser",
            "4 doser",
            "4 doser",
        ],
    }
)
fourth_dose = pd.concat([top_row_fourth, fourth_vacc_dose]).reset_index(drop=True)
fourth_dose = fourth_dose[fourth_dose.Åldersgrupp != "Totalt"]
fourth_dose = fourth_dose[fourth_dose.Åldersgrupp != "65-69"]

## Prepare dataframe for heatmap (all data in one place)

heatmap_data = pd.concat(
    [one_dose, two_doses, third_dose, fourth_dose],
    axis=0,
)
heatmap_data["Vaccinationsstatus"] = heatmap_data["Vaccinationsstatus"].replace(
    {
        "Minst 1 dos": "1",
        "Minst 2 doser": "2",
        "3 doser": "3",
        "4 doser": "4",
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

filename = os.path.join(os.getcwd(), "vaccine_plots", "vaccine_heatmap_small.json")
if not os.path.isdir(os.path.dirname(filename)):
    os.mkdir(os.path.dirname(filename))

fig_small.write_json(filename)
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

# fig.show()

filename = os.path.join(os.getcwd(), "vaccine_plots", "vaccine_heatmap.json")

fig.write_json(filename)
# fig.write_image("Plots/vaccine_heatmap.png")
