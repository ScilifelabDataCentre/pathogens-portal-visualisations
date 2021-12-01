import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np  # won't need this when data on 3rd dose for 12-17 year olds becomes available
import os

## Need 3 sets of data - for one dose, two doses, and three doses
## data for 3 doses is held separately - work with data for 1st 2 doses first
# Don't have population size data for these age groups (at least right now), so can't do population level calculations

df_vacc_age = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade ålder",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# initial processing
df_vacc_age = df_vacc_age.replace("| Sverige |", "Sweden")
df_vacc_age = df_vacc_age[(df_vacc_age["Region"] == "Sweden")]
df_vacc_age = df_vacc_age.replace("90 eller äldre", "90 and<br>above")
df_vacc_age = df_vacc_age.replace("80-89", "80 - 89")
df_vacc_age = df_vacc_age.replace("70-79", "70 - 79")
df_vacc_age = df_vacc_age.replace("60-69", "60 - 69")
df_vacc_age = df_vacc_age.replace("50-59", "50 - 59")
df_vacc_age = df_vacc_age.replace("40-49", "40 - 49")
df_vacc_age = df_vacc_age.replace("30-39", "30 - 39")
df_vacc_age = df_vacc_age.replace("18-29", "18 - 29")
df_vacc_age = df_vacc_age.replace("16-17", "16 - 17")
df_vacc_age = df_vacc_age.replace("12-15", "12 - 15")
df_vacc_age.drop(
    df_vacc_age[(df_vacc_age["Åldersgrupp"] == "Totalt")].index, inplace=True
)
df_vacc_age["Procent vaccinerade"] = df_vacc_age["Andel vaccinerade"] * 100

# Separate data for one and two doses

# one dose
one_dose = df_vacc_age[(df_vacc_age["Vaccinationsstatus"] == "Minst 1 dos")]
one_dose = one_dose[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
one_dose.reset_index(drop=True, inplace=True)

# data for two doses
two_doses = df_vacc_age[(df_vacc_age["Vaccinationsstatus"] == "Minst 2 doser")]
two_doses = two_doses[["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]]
two_doses.reset_index(drop=True, inplace=True)

## Sort data for three doses. Note - data only currently available for 18+ (from 12 for 1 & 2 dose)

vacc_third_age = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Dos 3 per åldersgrupp",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# initial processing
vacc_third_age = vacc_third_age.replace("| Sverige |", "Sweden")
vacc_third_age = vacc_third_age[(vacc_third_age["Region"] == "Sweden")]
vacc_third_age = vacc_third_age.replace("90 eller äldre", "90 and<br>above")
vacc_third_age = vacc_third_age.replace("80-89", "80 - 89")
vacc_third_age = vacc_third_age.replace("70-79", "70 - 79")
vacc_third_age = vacc_third_age.replace("60-69", "60 - 69")
vacc_third_age = vacc_third_age.replace("50-59", "50 - 59")
vacc_third_age = vacc_third_age.replace("40-49", "40 - 49")
vacc_third_age = vacc_third_age.replace("30-39", "30 - 39")
vacc_third_age = vacc_third_age.replace("18-29", "18 - 29")
vacc_third_age = vacc_third_age.replace("16-17", "16 - 17")
vacc_third_age = vacc_third_age.replace("12-15", "12 - 15")
vacc_third_age.drop(
    vacc_third_age[(vacc_third_age["Åldersgrupp"] == "Totalt")].index, inplace=True
)
vacc_third_age["Procent vaccinerade"] = vacc_third_age["Andel vaccinerade"] * 100
vacc_third_age = vacc_third_age[
    ["Åldersgrupp", "Procent vaccinerade", "Vaccinationsstatus"]
]

# adding a top row to third dose while no data for 12-15 and 16-17 age categories
## REMOVE THIS SECTION WHEN THESE AGE CATEGORIES ARE AVAILABLE FOR THIRD DOSE DATA
top_row = pd.DataFrame(
    {
        "Åldersgrupp": ["12 - 15", "16 - 17"],
        "Procent vaccinerade": [np.nan, np.nan],
        "Vaccinationsstatus": ["3 doser", "3 doser"],
    }
)
vacc_third_age = pd.concat([top_row, vacc_third_age]).reset_index(drop=True)

## DELETE TO HERE WHEN THIRD DOSE for 12-15 and 16-17 AVAILABLE

## Prepare DataFrames for heatmap (all data in one place)

# FoHM data first
heatmap_data = pd.concat(
    [one_dose, two_doses, vacc_third_age],
    axis=0,
)
heatmap_data["Vaccinationsstatus"] = heatmap_data["Vaccinationsstatus"].replace(
    {
        "Minst 1 dos": "At least 1 dose received",
        "Minst 2 doser": "At least 2 doses received",
        "3 doser": "3 doses received",
    }
)

## Make figure

colours = px.colors.diverging.RdBu

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
        "font_size": 16,
    }
)
fig.update_layout(
    title=" ",
    plot_bgcolor="white",
    yaxis={
        "title": "<b>Age Group<br></b>",
        "linecolor": "black",
    },
    font={"size": 16},
    # width=2000, # width not set - will depend on portal space
    height=1000,  # set height for portal (can remove if we want height to depend on space in pace)
    xaxis={
        "title": "<br><b>Vaccine Doses</b>",
        "tickangle": 0,
        "zeroline": True,
        "linecolor": "black",
    },
)

# add text annotation regarding no data

fig.add_annotation(
    xref="paper",  # yref="paper",
    x=1.125,
    y=4.30,
    text="<b>Note:</b> White<br>indicates no data",
    showarrow=False,
)

fig.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

fig.write_json("Plots/vaccine_heatmap.json")

### Now work based on population size calculations
