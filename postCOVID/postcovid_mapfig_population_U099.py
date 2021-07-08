import json
import pandas as pd
import plotly.express as px
import csv

# import requests


# map
with open("/Users/arnold/Documents/Covid_portal_vis/postCOVID/sweden-counties.geojson", "r") as sw:
    jdata = json.load(sw)

# dictionary to match data and map
counties_id_map = {}
for feature in jdata["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    counties_id_map[feature["properties"]["name"]] = feature["id"]

# data
df1 = pd.read_csv(
    "https://blobserver.dckube.scilifelab.se/blob/Summary_postcovid_statistics.csv",
    header=0,
)

# join data to map
df1["id"] = df1["Lan"].apply(lambda x: counties_id_map[x])

# colour theme
colour = px.colors.sequential.tempo
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]

# information related to languages
language = "English"

if language == "Swedish":
    cbtit = "procent folk U.09.9"
elif language == "English":
    cbtit = "Percentage of population which received the U09.9 diagnosis"
else:
    cbtit = "lang_error"

if language == "Swedish":
    perc_postcov_title = "Procent av folk"
elif language == "English":
    perc_postcov_title = "Percentage of population which received the U09.9 diagnosis"
else:
    perc_postcov_title = "lang_error"

if language == "Swedish":
    raw_number_title = "Antal postcovid fall"
elif language == "English":
    raw_number_title = "Number of people who received the U09.9 diagnosis"
else:
    raw_number_title = "lang_error"

if language == "Swedish":
    Population = "Folkmängd"
elif language == "English":
    Population = "Total population"
else:
    Population = "lang_error"


# # make figure
fig = px.choropleth(
    df1,
    geojson=jdata,
    locations="id",
    color=df1["proc_kodU099_pop"],
    # Below gives discrete colours
    color_continuous_scale=[
        (splits[0], colour[0]),
        (splits[1], colour[0]),
        (splits[1], colour[1]),
        (splits[2], colour[1]),
        (splits[2], colour[2]),
        (splits[3], colour[2]),
        (splits[3], colour[3]),
        (splits[4], colour[3]),
        (splits[4], colour[4]),
        (splits[5], colour[4]),
        (splits[5], colour[5]),
        (splits[6], colour[5]),
        (splits[6], colour[6]),
        (splits[7], colour[6]),
        (splits[7], colour[7]),
        (splits[8], colour[7]),
        (splits[8], colour[8]),
        (splits[9], colour[8]),
        (splits[9], colour[9]),
        (splits[10], colour[9]),
    ],
    # this keeps the range of colours constant regardless of data
    range_color=[0, 1.0],
    scope="europe",
    hover_name="Lan",
    labels={
        "proc_kodU099_pop": perc_postcov_title,
        "Antal_kodU099": raw_number_title,
        "Population": Population,
    },
    hover_data={
        "Population": True,
        "Antal_kodU099": True,
        "proc_kodU099_pop": True,
        "proc_kodU099_pop": ":.2f",
        "id": False,
    },
)
# this section deals with the exact focus on the map

lat_foc = 62.45
lon_foc = 22.5
fig.update_layout(
    geo=dict(
        lonaxis_range=[20, 90],  # the logitudinal range to consider
        projection_scale=4.55,  # this is kind of like zoom
        center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
        visible=False,
    )
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=255, height=348)
fig.update_layout(dragmode=False)
# The below labels the colourbar categories
fig.update_layout(
    coloraxis_colorbar=dict(
        title="<b>" + cbtit + "</b>",
        tickvals=[
            0.05,
            0.15,
            0.25,
            0.35,
            0.45,
            0.55,
            0.65,
            0.75,
            0.85,
            0.95,
        ],
        ticktext=[
            "0.00 - 0.10 %",
            "0.10 - 0.20 %",
            "0.20 - 0.30 %",
            "0.30 - 0.40 %",
            "0.40 - 0.50 %",
            "0.50 - 0.60 %",
            "0.60 - 0.70 %",
            "0.70 - 0.80 %",
            "0.80 - 0.90 %",
            "> 0.90 %",
        ],
        x=0.55,
        y=0.8,
        thicknessmode="pixels",
        thickness=10,
        lenmode="pixels",
        len=150,
    ),
    font=dict(size=9),
)
# write out as html for web
# fig.show()
fig.write_html(
    "map_postcovid_percent_of_population_U099.html",
    include_plotlyjs=True,
    full_html=True,
)
