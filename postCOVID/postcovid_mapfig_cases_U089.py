import json
import pandas as pd
import plotly.express as px
import csv

# map
with open("sweden-counties.geojson", "r") as sw:
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


# tie data and map
df1["id"] = df1["Lan"].apply(lambda x: counties_id_map[x])

# colour theme
colour = px.colors.sequential.tempo
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]

# language information
language = "English"

if language == "Swedish":
    cbtit = "Antal personer som fått<br>diagnosen U08.9/Z86.1A<br>relativt antal<br>bekräftade fall"
elif language == "English":
    cbtit = "Number of people that received<br>a U08.9 or Z86.1A diagnosis as<br>a percentage of confirmed<br>COVID-19 cases"
else:
    cbtit = "lang_error"

if language == "Swedish":
    perc_postcov_title = "<br>Antal personer som fått<br>diagnosen U08.9/Z86.1A<br>relativt antal<br>bekräftade fall"
elif language == "English":
    perc_postcov_title = "<br>Number of people that received<br>a U08.9 or Z86.1A diagnosis as<br>a percentage of confirmed<br>COVID-19 cases"
else:
    perc_postcov_title = "lang_error"

if language == "Swedish":
    raw_number_title = "<br>Antal personer som fått<br>diagnosen U08.9/Z86.1A"
elif language == "English":
    raw_number_title = (
        "<br>Number of people that received<br>a U08.9 or Z86.1A diagnosis"
    )
else:
    raw_number_title = "lang_error"

if language == "Swedish":
    covid_cases = "Kumulativt antal bekräftade<br>fall av Covid-19"
elif language == "English":
    covid_cases = "Cumulative number of<br>confirmed COVID-19 cases"
else:
    covid_cases = "lang_error"


# # make figure
fig = px.choropleth(
    df1,
    geojson=jdata,
    locations="id",
    color=df1["proc_kodU089_fall"],
    # Below gives discrete colours for ranges
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
    range_color=[0, 5.0],
    scope="europe",
    hover_name="Lan",
    labels={
        "proc_kodU089_fall": perc_postcov_title,
        "Antal_kodU089": raw_number_title,
        "Kum_antal_fall": covid_cases,
    },
    hover_data={
        "Kum_antal_fall": True,
        "Antal_kodU089": True,
        "proc_kodU089_fall": True,
        "proc_kodU089_fall": ":.2f",
        "id": False,
    },
)
# this section deals with the exact focus on the map

lat_foc = 62.45
lon_foc = 20.5
fig.update_layout(
    geo=dict(
        lonaxis_range=[20, 90],  # the logitudinal range to consider
        lataxis_range=[48, 100],  # the logitudinal range to consider
        projection_scale=4.55,  # this is kind of like zoom
        center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
        visible=False,
    )
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=400, height=500)
fig.update_layout(dragmode=False)
# The below labels the colourbar categories
fig.update_layout(
    coloraxis_colorbar=dict(
        title="<b>" + cbtit + "</b>",
        tickvals=[
            0.25,
            0.75,
            1.25,
            1.75,
            2.25,
            2.75,
            3.25,
            3.75,
            4.25,
            4.75,
        ],
        ticktext=[
            "0.00 - 0.50 %",
            "0.50 - 1.00 %",
            "1.00 - 1.50 %",
            "1.50 - 2.00 %",
            "2.00 - 2.50 %",
            "2.50 - 3.00 %",
            "3.00 - 3.50 %",
            "3.50 - 4.00 %",
            "4.00 - 4.50 %",
            "> 4.50 %",
        ],
        x=0.51,
        y=0.40,
        thicknessmode="pixels",
        thickness=10,
        lenmode="pixels",
        len=195,
    ),
    font=dict(size=9),
)
# fig.update_layout(coloraxis_colorbar_x=0.53, coloraxis_colorbar_y=0.53)
# write out as html for web
# fig.show()
fig.write_json("map_postcovid_percent_of_covidcases_U089_{}.json".format(language))
