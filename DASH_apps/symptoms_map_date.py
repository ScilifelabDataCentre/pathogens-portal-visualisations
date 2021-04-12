import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import json
import requests
import csv
import pandas as pd
from datetime import datetime as dt


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
data = list(reader)
df1 = pd.DataFrame(data)
df1.columns = df1.iloc[0]
df1 = df1.reindex(df1.index.drop(0)).reset_index(drop=True)
df1.columns.name = None

# format data
df1["Datum"] = pd.to_datetime(df1["Datum"])  # .dt.date
# df1["Datum"] = df1["Datum"].dt.strftime("%Y-%m-%d")
df1["Uppskattning"] = pd.to_numeric(df1["Uppskattning"], errors="coerce")
df1["Uppskattning"] = df1["Uppskattning"].fillna(-0.1)
# comment out next row when Dalarna fixed
df1["Lan"] = df1["Lan"].replace("Dalar", "Dalarna")
df1["id"] = df1["Lan"].apply(lambda x: counties_id_map[x])

# colour theme
colour = px.colors.sequential.tempo
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]

df1["Uppskattning_Lan"] = df1["Uppskattning"].astype(str)
df1["Uppskattning_Lan"].replace(str(-0.1), "Insufficient data", inplace=True)

# create the app layout

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1("COVID-19 test dashboard"),
        html.P(
            [
                html.Label("Date"),
                html.Label("(Day/Month/Year)"),
                dcc.DatePickerSingle(
                    id="date_pick",
                    min_date_allowed=dt(2020, 5, 11).date(),
                    max_date_allowed=df1["Datum"].iloc[-1],
                    initial_visible_month=df1["Datum"].iloc[-1],
                    date=df1["Datum"].iloc[-1],
                    display_format=("DD/MM/YYYY"),
                    # dt(2021, 4, 7).date(),  # pd.to_datetime("today").date(),
                ),
                dcc.Graph(id="choropleth"),
            ]
        ),
    ]
)

# make app callback (figure generated in update)
@app.callback(Output("choropleth", "figure"), [Input("date_pick", "date")])
def update_choropleth(input_date):
    df = df1[(df1["Datum"] == input_date)]
    mapdata = jdata
    colour = px.colors.sequential.tempo
    splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
    fig = px.choropleth(
        df,
        geojson=mapdata,
        locations="id",
        color=df["Uppskattning"],
        scope="europe",
        range_color=[-0.1, 0.90],
        # range_color=[-0.1, 1.0],
        hover_name="Lan",
        labels={"Uppskattning_Lan": "Estimated prevalence"},
        hover_data={"Uppskattning_Lan": True, "Uppskattning": False, "id": False},
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
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=510, height=696)
    fig.update_layout(
        geo=dict(
            lonaxis_range=[20, 90],  # the logitudinal range to consider
            projection_scale=4.55,  # this is kind of like zoom
            center=dict(lat=55.45, lon=22.5),  # this will center on the point
            visible=False,
        )
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="<b>"
            + "Estimated prevalence of<br>symptomatic cases,<br>percentage of respondants"
            + "</b>"
            + "<br>(updated daily)",
            tickvals=[
                -0.050,
                0.050,
                0.150,
                0.250,
                0.350,
                0.450,
                0.550,
                0.650,
                0.750,
                0.850,
            ],
            ticktext=[
                "Insufficient data",
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
            x=0.0,
            y=0.8,
            thicknessmode="pixels",
            thickness=10,
            lenmode="pixels",
            len=250,
        ),
        font=dict(size=12),
    )
    return fig


# server clause

app.run_server(debug=True)