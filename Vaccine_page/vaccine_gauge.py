# This will make the 'loading bars' for vaccines.
# script sits independently - no currrent plans to use
# Need to test view on page when in json format, sometimes indicators display strangely
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime as dt
from datetime import timedelta

## Import and sort data from Folkhälsomyndigheten
## initially deal with data from first two doses

df_vacc = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Vaccinerade tidsserie",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

## DO we want to align with case data on vaccinations page?

# # backdate vaccine data to align with the case data
# df_vacc_fill = pd.read_excel(
#     "vaccine_fill_data.xlsx",
#     sheet_name="Sheet 1",
#     header=0,
#     engine="openpyxl",
#     keep_default_na=False,
# )

# df_vacc = pd.concat([df_vacc_fill, df_vacc])

df_vacc["day"] = 4  # set day as Thursday (when public health data is updated)

df_vacc["date"] = df_vacc.apply(
    lambda row: dt.fromisocalendar(row["År"], row["Vecka"], row["day"]), axis=1
)

df_vacc = df_vacc.replace("| Sverige |", "Sweden")

df_vacc["Andel vaccinerade"] = df_vacc["Andel vaccinerade"].replace(
    ",", ".", regex=True
)

df_vacc["Procent vaccinerade"] = (df_vacc["Andel vaccinerade"].astype(float)) * 100

df_vacc = df_vacc[
    ["date", "Region", "Antal vaccinerade", "Procent vaccinerade", "Vaccinationsstatus"]
]

# only need values for Sweden, so limit the data set

df_vacc = df_vacc[(df_vacc["Region"] == "Sweden")]

one_dose_swe = df_vacc[
    (df_vacc["Region"] == "Sweden")
    & (df_vacc["date"] == df_vacc["date"].max())
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

# print(one_dose_swe)
one_dose_swe = float(one_dose_swe["Procent vaccinerade"].round(2))

one_dose_lastweek = df_vacc[
    (df_vacc["Region"] == "Sweden")
    & (df_vacc["date"] == df_vacc["date"].unique()[-2])
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

# print(one_dose_lastweek)
one_dose_lastweek = float(one_dose_lastweek["Procent vaccinerade"].round(2))

one_dose_twoweek = df_vacc[
    (df_vacc["Region"] == "Sweden")
    & (df_vacc["date"] == df_vacc["date"].unique()[-3])
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

# print(one_dose_twoweek)
one_dose_twoweek = float(one_dose_twoweek["Procent vaccinerade"].round(2))

least_two_dose_swe = df_vacc[
    (df_vacc["Region"] == "Sweden")
    & (df_vacc["date"] == df_vacc["date"].max())
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

# print(least_two_dose_swe)
least_two_dose_swe = float(least_two_dose_swe["Procent vaccinerade"].round(2))

least_two_dose_lastweek = df_vacc[
    (df_vacc["Region"] == "Sweden")
    & (df_vacc["date"] == df_vacc["date"].unique()[-2])
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

# print(least_two_dose_lastweek)
least_two_dose_lastweek = float(least_two_dose_lastweek["Procent vaccinerade"].round(2))

least_two_dose_twoweek = df_vacc[
    (df_vacc["Region"] == "Sweden")
    & (df_vacc["date"] == df_vacc["date"].unique()[-3])
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

# print(least_two_dose_twoweek)
least_two_dose_twoweek = float(least_two_dose_twoweek["Procent vaccinerade"].round(2))

## Now work out rates
rate_onedose_lastwk = float("{:.2f}".format(one_dose_swe - one_dose_lastweek))
rate_onedose_twowk = float("{:.2f}".format(one_dose_lastweek - one_dose_twoweek))
rate_leasttwodose_lastwk = float(
    "{:.2f}".format(least_two_dose_swe - least_two_dose_lastweek)
)
rate_leasttwodose_twowk = float(
    "{:.2f}".format(least_two_dose_lastweek - least_two_dose_twoweek)
)

## Now data for 3rd dose (not currently included in time series)
## may need to note that 'at least 2 doses COULD include 3rd dose'...

third_vacc_dose = pd.read_excel(
    "https://fohm.maps.arcgis.com/sharing/rest/content/items/fc749115877443d29c2a49ea9eca77e9/data",
    sheet_name="Dos 3 per åldersgrupp",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

third_vacc_dose = third_vacc_dose.replace("| Sverige |", "Sweden")

third_vacc_dose["Andel vaccinerade"] = third_vacc_dose["Andel vaccinerade"].replace(
    ",", ".", regex=True
)

third_vacc_dose["Procent vaccinerade"] = (
    third_vacc_dose["Andel vaccinerade"].astype(float)
) * 100

# only have total number for now, so no rate calculations etc. for now
third_vacc_dose_tot = third_vacc_dose[
    (third_vacc_dose["Åldersgrupp"] == "Totalt")
    & (third_vacc_dose["Region"] == "Sweden")
]

third_vacc_dose_tot = float(third_vacc_dose_tot["Procent vaccinerade"].round(2))
# print(third_vacc_dose_tot)

## Make figures

# Add the first figure

Vacc_doses = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=one_dose_swe,
        title={
            "text": "At least <b>one</b> dose",
            "font": {
                "size": 30
            },  # "<b>Percentage of population that<br>received at least 1 dose<br></b>"
        },
        gauge={
            "axis": {
                "range": [None, 100],
                "ticksuffix": "%",
                "tickfont": {"size": 35},
                "showticklabels": False,
            },
            "shape": "bullet",
        },
        #         'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
        number={"font": {"size": 50}, "suffix": "%"},
        domain={"x": [0, 1], "y": [0.65, 1]},
    )
)

Vacc_doses.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=least_two_dose_swe,
        title={
            "text": "At least <b>two</b> doses",
            "font": {
                "size": 30
            },  # "<b>Percentage of population that<br>received at least 1 dose<br></b>"
        },
        gauge={
            "axis": {
                "range": [None, 100],
                "ticksuffix": "%",
                "tickfont": {"size": 35},
                "showticklabels": False,
            },
            "shape": "bullet",
        },
        #         'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
        number={"font": {"size": 50}, "suffix": "%"},
        domain={"x": [0, 1], "y": [0.35, 0.65]},
    )
)

Vacc_doses.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=third_vacc_dose_tot,
        title={
            "text": "Received <b>three</b> doses",
            "font": {
                "size": 30
            },  # "<b>Percentage of population that<br>received at least 1 dose<br></b>"
        },
        gauge={
            "axis": {"range": [None, 100], "ticksuffix": "%", "tickfont": {"size": 35}},
            "shape": "bullet",
        },
        #         'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
        number={"font": {"size": 50}, "suffix": "%"},
        domain={"x": [0, 1], "y": [0, 0.35]},
    )
)

Vacc_doses.update_layout(height=500, margin={"l": 500})
Vacc_doses.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

Vacc_doses.write_json("Plots/vaccine_indicator.json")
# png displays strangely
# Vacc_doses.write_image("Plots/vaccine_indicator.png")
