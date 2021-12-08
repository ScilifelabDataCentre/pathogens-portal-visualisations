import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

from vaccine_dataprep_Swedentots import (
    df_vacc_lan,  # data on 1st 2 doses
    third_vacc_dose_lan,  # data on 3rd dose
    # df_vacc_ålders_lan,  # a switch to age data for 1st and second doses?
)

# map
with open("sweden-counties.geojson", "r") as sw:
    jdata = json.load(sw)

# dictionary to match data and map
counties_id_map = {}
for feature in jdata["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    counties_id_map[feature["properties"]["name"]] = feature["id"]

# data to match to map (make 3 maps ultimately, with each data frame linked to a new map)

# df_vacc_lan = df_vacc_ålders_lan #if we switch, we need to do this and get rid of date stuff and switch to using totals instead

# first two doses

one_dose_lan = df_vacc_lan[
    (df_vacc_lan["date"] == df_vacc_lan["date"].max())
    # (df_vacc_lan["Åldersgrupp"] == "Totalt")
    & (df_vacc_lan["Vaccinationsstatus"] == "Minst 1 dos")
]

one_dose_lan.drop(
    one_dose_lan[(one_dose_lan["Region"] == "Sweden")].index, inplace=True
)

one_dose_lan = one_dose_lan.replace("Minst 1 dos", "One dose")

two_dose_lan = df_vacc_lan[
    (df_vacc_lan["date"] == df_vacc_lan["date"].max())
    # (df_vacc_lan["Åldersgrupp"] == "Totalt")
    & (df_vacc_lan["Vaccinationsstatus"] == "Minst 2 doser")
]

two_dose_lan.drop(
    two_dose_lan[(two_dose_lan["Region"] == "Sweden")].index, inplace=True
)

two_dose_lan = two_dose_lan.replace("Minst 2 doser", "Two doses")

# third dose

third_vacc_dose_lan = third_vacc_dose_lan[
    (third_vacc_dose_lan["Åldersgrupp"] == "Totalt")
]

third_vacc_dose_lan.drop(
    third_vacc_dose_lan[(third_vacc_dose_lan["Region"] == "Sweden")].index, inplace=True
)

third_vacc_dose_lan = third_vacc_dose_lan.replace("3 doser", "Three doses")

# Tie each dataframe to the map
# one dose
one_dose_lan["id"] = one_dose_lan["Region"].apply(lambda x: counties_id_map[x])
# two doses
two_dose_lan["id"] = two_dose_lan["Region"].apply(lambda x: counties_id_map[x])
# three doses
third_vacc_dose_lan["id"] = third_vacc_dose_lan["Region"].apply(
    lambda x: counties_id_map[x]
)

map_colour = px.colors.diverging.RdBu
map_colour[5] = "rgb(255,255,204)"
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
lat_foc = 62.45
lon_foc = 20.5

# One dose (FoHm data)

one_FoHm_map_plot = px.choropleth(
    one_dose_lan,
    geojson=jdata,
    locations="id",
    color=one_dose_lan["Procent vaccinerade"],
    # Below gives discrete colours for ranges
    color_continuous_scale=[
        (splits[0], map_colour[10]),
        (splits[1], map_colour[10]),
        (splits[1], map_colour[9]),
        (splits[2], map_colour[9]),
        (splits[2], map_colour[8]),
        (splits[3], map_colour[8]),
        (splits[3], map_colour[7]),
        (splits[4], map_colour[7]),
        (splits[4], map_colour[6]),
        (splits[5], map_colour[6]),
        (splits[5], map_colour[5]),
        (splits[6], map_colour[5]),
        (splits[6], map_colour[4]),
        (splits[7], map_colour[4]),
        (splits[7], map_colour[3]),
        (splits[8], map_colour[3]),
        (splits[8], map_colour[2]),
        (splits[9], map_colour[2]),
        (splits[9], map_colour[1]),
        (splits[10], map_colour[1]),
    ],
    # this keeps the range of colours constant regardless of data
    range_color=[0, 100],
    scope="europe",
    hover_name="Region",
    hover_data={
        "Procent vaccinerade": ":.2f",
        "Vaccinationsstatus": True,  # ":.2f",
        "id": False,
    },
    labels={
        "Procent vaccinerade": "Percentage<br>Vaccinated (%)",
        "Vaccinationsstatus": "<br>Number of Doses",
    },
)
# this section deals with the exact focus on the map
one_FoHm_map_plot.update_layout(
    geo=dict(
        lonaxis_range=[20, 90],  # the logitudinal range to consider
        lataxis_range=[48, 100],  # the logitudinal range to consider
        projection_scale=4.55,  # this is kind of like zoom
        center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
        visible=False,
    )
)
one_FoHm_map_plot.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800)
one_FoHm_map_plot.update_layout(dragmode=False)
# The below labels the colourbar categories
one_FoHm_map_plot.update_layout(
    coloraxis_colorbar=dict(
        title="<b>" + "Percentage vaccinated<br>with one dose (FoHM)" + "</b>",
        tickvals=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
        ticktext=[
            "00.00 - 9.99 %",
            "10.00 - 19.99 %",
            "20.00 - 29.99 %",
            "30.00 - 39.00 %",
            "40.00 - 49.99 %",
            "50.00 - 59.99 %",
            "60.00 - 69.99 %",
            "70.00 - 79.99 %",
            "80.00 - 89.99 %",
            "90.00 - 100.00 %",
        ],
        x=0.51,
        y=0.40,
        thicknessmode="pixels",
        thickness=10,
        lenmode="pixels",
        len=285,
    ),
    font=dict(size=14),
)
one_FoHm_map_plot.update_traces(marker_line_color="white")
one_FoHm_map_plot.show()

# two doses (FoHm data)

two_FoHm_map_plot = px.choropleth(
    two_dose_lan,
    geojson=jdata,
    locations="id",
    color=two_dose_lan["Procent vaccinerade"],
    # Below gives discrete colours for ranges
    color_continuous_scale=[
        (splits[0], map_colour[10]),
        (splits[1], map_colour[10]),
        (splits[1], map_colour[9]),
        (splits[2], map_colour[9]),
        (splits[2], map_colour[8]),
        (splits[3], map_colour[8]),
        (splits[3], map_colour[7]),
        (splits[4], map_colour[7]),
        (splits[4], map_colour[6]),
        (splits[5], map_colour[6]),
        (splits[5], map_colour[5]),
        (splits[6], map_colour[5]),
        (splits[6], map_colour[4]),
        (splits[7], map_colour[4]),
        (splits[7], map_colour[3]),
        (splits[8], map_colour[3]),
        (splits[8], map_colour[2]),
        (splits[9], map_colour[2]),
        (splits[9], map_colour[1]),
        (splits[10], map_colour[1]),
    ],
    # this keeps the range of colours constant regardless of data
    range_color=[0, 100],
    scope="europe",
    hover_name="Region",
    hover_data={
        "Procent vaccinerade": ":.2f",
        "Vaccinationsstatus": True,  # ":.2f",
        "id": False,
    },
    labels={
        "Procent vaccinerade": "Percentage<br>Vaccinated (%)",
        "Vaccinationsstatus": "<br>Number of Doses",
    },
)
# this section deals with the exact focus on the map
two_FoHm_map_plot.update_layout(
    geo=dict(
        lonaxis_range=[20, 90],  # the logitudinal range to consider
        lataxis_range=[48, 100],  # the logitudinal range to consider
        projection_scale=4.55,  # this is kind of like zoom
        center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
        visible=False,
    )
)
two_FoHm_map_plot.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800)
two_FoHm_map_plot.update_layout(dragmode=False)
# The below labels the colourbar categories
two_FoHm_map_plot.update_layout(
    coloraxis_colorbar=dict(
        title="<b>" + "Percentage vaccinated<br>with two doses (FoHM)" + "</b>",
        tickvals=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
        ticktext=[
            "00.00 - 9.99 %",
            "10.00 - 19.99 %",
            "20.00 - 29.99 %",
            "30.00 - 39.00 %",
            "40.00 - 49.99 %",
            "50.00 - 59.99 %",
            "60.00 - 69.99 %",
            "70.00 - 79.99 %",
            "80.00 - 89.99 %",
            "90.00 - 100.00 %",
        ],
        x=0.51,
        y=0.40,
        thicknessmode="pixels",
        thickness=10,
        lenmode="pixels",
        len=285,
    ),
    font=dict(size=14),
)
two_FoHm_map_plot.update_traces(marker_line_color="white")
two_FoHm_map_plot.show()

# three doses FoHM data

three_FoHm_map_plot = px.choropleth(
    third_vacc_dose_lan,
    geojson=jdata,
    locations="id",
    color=third_vacc_dose_lan["Procent vaccinerade"],
    # Below gives discrete colours for ranges
    color_continuous_scale=[
        (splits[0], map_colour[10]),
        (splits[1], map_colour[10]),
        (splits[1], map_colour[9]),
        (splits[2], map_colour[9]),
        (splits[2], map_colour[8]),
        (splits[3], map_colour[8]),
        (splits[3], map_colour[7]),
        (splits[4], map_colour[7]),
        (splits[4], map_colour[6]),
        (splits[5], map_colour[6]),
        (splits[5], map_colour[5]),
        (splits[6], map_colour[5]),
        (splits[6], map_colour[4]),
        (splits[7], map_colour[4]),
        (splits[7], map_colour[3]),
        (splits[8], map_colour[3]),
        (splits[8], map_colour[2]),
        (splits[9], map_colour[2]),
        (splits[9], map_colour[1]),
        (splits[10], map_colour[1]),
    ],
    # this keeps the range of colours constant regardless of data
    range_color=[0, 100],
    scope="europe",
    hover_name="Region",
    hover_data={
        "Procent vaccinerade": ":.2f",
        "Vaccinationsstatus": True,  # ":.2f",
        "id": False,
    },
    labels={
        "Procent vaccinerade": "Percentage<br>Vaccinated (%)",
        "Vaccinationsstatus": "<br>Number of Doses",
    },
)
# this section deals with the exact focus on the map
three_FoHm_map_plot.update_layout(
    geo=dict(
        lonaxis_range=[20, 90],  # the logitudinal range to consider
        lataxis_range=[48, 100],  # the logitudinal range to consider
        projection_scale=4.55,  # this is kind of like zoom
        center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
        visible=False,
    )
)
three_FoHm_map_plot.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800)
three_FoHm_map_plot.update_layout(dragmode=False)
# The below labels the colourbar categories
three_FoHm_map_plot.update_layout(
    coloraxis_colorbar=dict(
        title="<b>" + "Percentage vaccinated<br>with three doses (FoHM)" + "</b>",
        tickvals=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
        ticktext=[
            "00.00 - 9.99 %",
            "10.00 - 19.99 %",
            "20.00 - 29.99 %",
            "30.00 - 39.00 %",
            "40.00 - 49.99 %",
            "50.00 - 59.99 %",
            "60.00 - 69.99 %",
            "70.00 - 79.99 %",
            "80.00 - 89.99 %",
            "90.00 - 100.00 %",
        ],
        x=0.51,
        y=0.40,
        thicknessmode="pixels",
        thickness=10,
        lenmode="pixels",
        len=285,
    ),
    font=dict(size=14),
)
three_FoHm_map_plot.update_traces(marker_line_color="white")
three_FoHm_map_plot.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

# # write out FoHM graphs
# one_FoHm_map_plot.write_json("Plots/onedose_FoHM_map.json")
# two_FoHm_map_plot.write_json("Plots/twodose_FoHM_map.json")
# three_FoHm_map_plot.write_json("Plots/threedose_FoHM_map.json")
