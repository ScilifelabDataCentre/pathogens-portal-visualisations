# Produces interactive map to show positions of wastewater treatment plants and relative levels of SARS-CoV-2
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import json
import numpy as np

df = pd.read_csv(
    "data/test_map_points.csv",
    sep=";",
    header=0,
)

df1 = pd.read_csv(
    "data/wastewater_basemap.csv",
    sep=";",
    header=0,
)

# map
with open("sweden-counties.geojson", "r") as sw:
    jdata = json.load(sw)

# dictionary to match data and map
counties_id_map = {}
for feature in jdata["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    counties_id_map[feature["properties"]["name"]] = feature["id"]


df["rank"] = np.nan
df["rank"] = (
    df["rank"]
    .mask(df.value == 1, "Low")
    .mask(df.value == 2, "Medium")
    .mask(df.value == 3, "High")
)

colour = px.colors.sequential.tempo
splits = [0.00, 0.50, 1.00]

# language = "Swedish"

# if language == "Swedish":
#     cbtit = "<b>Uppskattad förekomst av<br>symptomatisk Covid-19,<br>% av befolkningen</b><br>(uppdateras dagligen)"
# elif language == "English":
#     cbtit = "<b>Estimated prevalence of<br>symptomatic cases,<br>% of population</b><br>(updated daily)"
# else:
#     cbtit = "lang_error"
# if language == "Swedish":
#     overwrite = "Uppskattning<br>för Län (%) "
# elif language == "English":
#     overwrite = "Estimate<br>for County (%) "
# else:
#     overwrite = "lang_error"
# if language == "Swedish":
#     insuff = "<br>Otillräckligt<br>underlag"
# elif language == "English":
#     insuff = "Insufficient data"
# else:
#     cbtit = "lang_error"

df1["id"] = df1["Lan"].apply(lambda x: counties_id_map[x])

fig = px.choropleth(
    df1,
    geojson=jdata,
    locations="id",
    color=df1["plant_or_not"],
    # Below gives discrete colours for ranges of Uppskattning values
    color_continuous_scale=[
        (splits[0], "#E4FAE4"),
        (splits[1], "#E4FAE4"),
        (splits[1], "#E4FAE4"),
        (splits[2], "#E4FAE4"),
    ],
    # this keeps the range of colours constant regrdless of data
    range_color=[-1.1, 1.1],
    scope="europe",
    hover_name="Lan",
    # labels={"Uppskattning_Lan": overwrite},
    hover_data={"id": False, "plant_or_not": False},
)
# this section deals with the exact focus on the map
lat_foc = 62.45
lon_foc = 20.5
fig.update_layout(
    geo=dict(
        lonaxis_range=[20, 90],  # the logitudinal range to consider
        lataxis_range=[48, 100],  # the latitudinal range to consider
        projection_scale=4.55,  # this is kind of like zoom
        center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
        visible=False,
    )
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_coloraxes(showscale=False)
# fig.show()
# to save the figure
# fig.write_json("Symptoms_map_{}.json".format(language))


# # to write the file as .json
# map_func(df1, jdata, "English")
# map_func(df1, jdata, "Swedish")

fig.add_traces(
    data=go.Scattergeo(
        lon=df["long"],
        lat=df["lat"],
        mode="markers",
        marker=dict(
            color=px.colors.sequential.RdBu[10],  # df["value"],
            # color_continuous_scale=[
            # ],
            # colorscale=[
            #     (0, px.colors.sequential.RdBu[10]),
            #     (0.33, px.colors.sequential.RdBu[10]),
            #     (0.33, "yellow"),
            #     (0.66, "yellow"),
            #     (0.66, px.colors.sequential.RdBu[0]),
            #     (1.0, px.colors.sequential.RdBu[0]),
            # ],
            size=10,
            line=dict(color="black", width=2),
            # colorbar=dict(
            #     title="<b>Relative copy<br>number of SARS-CoV-2<br>to PMMoV</b>",
            #     tickvals=[1.33, 2.0, 2.66],
            #     ticktext=[
            #         "Low",
            #         "Medium",
            #         "High",
            #     ],
            #     x=0.55,
            #     y=0.8,
            #     thicknessmode="pixels",
            #     thickness=10,
            #     lenmode="pixels",
            #     len=250,
            # ),
        ),
        customdata=df,
        hovertemplate="<b>%{customdata[0]}</b><extra></extra>",  # <br><br>Population: %{customdata[4]} <br>Value: %{customdata[3]} <br>Classification: %{customdata[6]}<extra></extra>",
    )
)

fig.update_layout(font=dict(size=16))
fig.update_layout(dragmode=False)
# Prints as a json file
fig.write_json("wastewater_map_test.json")

fig.show()
