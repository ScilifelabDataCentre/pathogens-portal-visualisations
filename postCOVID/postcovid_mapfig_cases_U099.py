import json
import pandas as pd
import plotly.express as px
import csv
import os
import argparse

aparser = argparse.ArgumentParser(description="Generate map file for U099 cases")
aparser.add_argument("--output-dir", nargs="?", default="postcovid_plots",
                     help="Output directory where the files will be saved")
args = aparser.parse_args()

# map
with open(os.path.join(os.path.dirname(__file__), "sweden-counties.geojson"), "r") as sw:
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


# tie map and data
df1["id"] = df1["Lan"].apply(lambda x: counties_id_map[x])

# colour theme
colour = px.colors.diverging.RdBu
colour[5] = "rgb(255, 234, 0)"
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]


for language in ["English", "Swedish"]:
    if language == "English":
        cbtit = "Number of people that received<br>a U09.9 diagnosis as<br>a percentage of confirmed<br>COVID-19 cases"
        perc_postcov_title = "<br>Number of people that received<br>a U09.9 diagnosis as<br>a percentage of confirmed<br>COVID-19 cases"
        raw_number_title = "<br>Number of people that received<br>a U09.9 diagnosis"
        covid_cases = "Cumulative number of<br>confirmed COVID-19 cases"
        filename = "map_postcovid_percent_of_covidcases_U099.json"
    elif language == "Swedish":
        cbtit = "Antal personer som fått<br>diagnosen U09.9<br>relativt antal<br>bekräftade fall"
        perc_postcov_title = "<br>Antal personer som fått<br>diagnosen U09.9<br>relativt antal<br>bekräftade fall"
        raw_number_title = "<br>Antal personer som fått<br>diagnosen U09.9"
        covid_cases = "Kumulativt antal bekräftade<br>fall av Covid-19"
        filename = "map_postcovid_percent_of_covidcases_U099_{}.json".format(language)

    # # make figure
    fig = px.choropleth(
        df1,
        geojson=jdata,
        locations="id",
        color=df1["proc_kodU099_fall"],
        # Below gives discrete colours
        color_continuous_scale=[
            (splits[0], colour[9]),
            (splits[1], colour[9]),
            (splits[1], colour[8]),
            (splits[2], colour[8]),
            (splits[2], colour[7]),
            (splits[3], colour[7]),
            (splits[3], colour[6]),
            (splits[4], colour[6]),
            (splits[4], colour[5]),
            (splits[5], colour[5]),
            (splits[5], colour[4]),
            (splits[6], colour[4]),
            (splits[6], colour[3]),
            (splits[7], colour[3]),
            (splits[7], colour[2]),
            (splits[8], colour[2]),
            (splits[8], colour[1]),
            (splits[9], colour[1]),
            (splits[9], colour[0]),
            (splits[10], colour[0]),
        ],
        # this keeps the range of colours constant regardless of data
        range_color=[0, 5.0],
        scope="europe",
        hover_name="Lan",
        labels={
            "Kum_antal_fall": covid_cases,
            "Antal_kodU099": raw_number_title,
            "proc_kodU099_fall": perc_postcov_title,
        },
        hover_data={
            "Kum_antal_fall": True,
            "Antal_kodU099": True,
            "proc_kodU099_fall": True,
            "proc_kodU099_fall": ":.2f",
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
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )  # , width=400, height=500)
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
            len=230,
        ),
        font=dict(size=12),
    )
    # write out as html for web
    # fig.show()
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    fig.write_json(os.path.join(args.output_dir, filename))
