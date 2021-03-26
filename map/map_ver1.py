"""Maps values onto a county-level map of Sweden"""
import json
import pandas as pd
import plotly.express as px
import csv
import requests

# map
with open("sweden-counties.geojson", "r") as sw:
    jdata = json.load(sw)

# dictionary to match data and map
counties_id_map = {}
for feature in jdata["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    counties_id_map[feature["properties"]["name"]] = feature["id"]

# data
req = requests.get("https://urls.dckube.scilifelab.se/goto/csss/")
reader = csv.reader(req.text.splitlines())
data = list(reader)[-21:]
df1 = pd.DataFrame(
    data[0:], columns=["Lan", "Datum", "Uppskattning", "Low_CI", "High_CI"]
)

# format data
df1["Datum"] = pd.to_datetime(df1["Datum"])
df1.sort_values(by="Datum", ascending=False, inplace=True)
df1.drop_duplicates("Lan", keep="first", inplace=True)
df1["Uppskattning"] = pd.to_numeric(df1["Uppskattning"], errors="coerce")
df1["Uppskattning"] = df1["Uppskattning"].fillna(-0.1)
# comment out next row when Dalarna fixed
df1["Lan"] = df1["Lan"].replace("Dalar", "Dalarna")
df1["id"] = df1["Lan"].apply(lambda x: counties_id_map[x])

# colour theme
colour = px.colors.sequential.tempo
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]

language = "Swedish"

if language == "Swedish":
    cbtit = "Uppskattning"
elif language == "English":
    cbtit = "Estimate"
else:
    cbtit = "lang_error"

if language == "Swedish":
    insuff = "Otillräckligt underlag"
elif language == "English":
    insuff = "Insufficient data"
else:
    cbtit = "lang_error"


# make figure
fig = px.choropleth(
    df1,
    geojson=jdata,
    locations="id",
    color=df1["Uppskattning"],
    # Below gives discrete colours for ranges of Uppskattning values
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
    # this keeps the range of colours constant regrdless of data
    range_color=[-0.1, 1],
    scope="europe",
    hover_name="Lan",
    labels={"Uppskattning": cbtit, "id": "ID"},
    hover_data=["Uppskattning"],
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
# The below labels the colourbar, essentially categorises Uppskattning
fig.update_layout(
    coloraxis_colorbar=dict(
        title="<b>" + cbtit + "</b>",
        tickvals=[
            -0.045,
            0.065,
            0.175,
            0.285,
            0.395,
            0.505,
            0.615,
            0.725,
            0.835,
            0.945,
        ],
        ticktext=[
            insuff,
            "0.00 - 0.10 %",
            "0.10 - 0.20 %",
            "0.20 - 0.30 %",
            "0.30 - 0.40 %",
            "0.40 - 0.50 %",
            "0.50 - 0.60 %",
            "0.60 - 0.70 %",
            "0.70 - 0.80 %",
            "> 0.80 %",
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
# to 'show' the figure in browser
fig.show()
# to write the file as .png
# fig.write_image('map_with_factor.png', scale=2)
# write out as html for web
# fig.write_html("map_with_factor.html", include_plotlyjs=False, full_html=False)
