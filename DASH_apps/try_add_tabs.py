import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import csv
import pandas as pd
from datetime import datetime as dt


# data import and sort
df1 = pd.read_excel(
    "https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data",
    sheet_name="Veckodata Region",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

df1["day"] = 4  # set day as Thursday (when public health data is updated)

df1["date"] = df1.apply(
    lambda row: dt.fromisocalendar(row["år"], row["veckonummer"], row["day"]), axis=1
)

df1_fall = df1[["date", "Region", "Antal_fall_vecka"]]

df1_swe = df1_fall.groupby(["date"]).sum().reset_index()

df1_swe.insert(loc=1, column="Region", value="Sweden")

df1_fall = pd.concat([df1_fall, df1_swe])

df1_intense = df1[["date", "Region", "Antal_intensivvårdade_vecka"]]

dfi_swe = df1_intense.groupby(["date"]).sum().reset_index()

dfi_swe.insert(loc=1, column="Region", value="Sweden")

df1_intense = pd.concat([df1_intense, dfi_swe])

server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

tab1 = html.Div(
    [
        html.H1("Number of COVID-19 cases each week"),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            [
                                html.Label("Select TimeFrame"),
                                html.Label("(Start Date and End Date)"),
                                dcc.DatePickerRange(
                                    id="my-date-picker-range",  # ID to be used for callback
                                    calendar_orientation="horizontal",  # vertical or horizontal
                                    day_size=39,  # size of calendar image. Default is 39
                                    end_date_placeholder_text="Return",  # text that appears when no end date chosen
                                    with_portal=False,  # if True calendar will open in a full screen overlay portal
                                    first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                                    reopen_calendar_on_clear=True,
                                    is_RTL=False,  # True or False for direction of calendar
                                    clearable=True,  # whether or not the user can clear the dropdown
                                    number_of_months_shown=1,  # number of months shown when calendar is open
                                    min_date_allowed=df1_fall["date"].iloc[
                                        0
                                    ],  # minimum date allowed on the DatePickerRange component
                                    max_date_allowed=df1_fall["date"].iloc[-1],
                                    initial_visible_month=df1_fall["date"].iloc[-1],
                                    start_date=df1_fall["date"].iloc[0],
                                    end_date=df1_fall["date"].iloc[-1],
                                    display_format="DD MMM YY",  # how selected dates are displayed in the DatePickerRange component.
                                    month_format="MMMM, YYYY",  # how calendar headers are displayed when the calendar is opened.
                                    minimum_nights=1,  # minimum number of days between start and end date
                                    persistence=True,
                                    persisted_props=["start_date"],
                                    persistence_type="session",  # session, local, or memory. Default is 'local'
                                    updatemode="singledate",  # singledate or bothdates. Determines when callback is triggered
                                ),
                            ]
                        ),
                        html.Div(
                            html.P(
                                [
                                    html.Label(
                                        "Select County (whole of Sweden shown by default)"
                                    ),
                                    dcc.Dropdown(
                                        id="county-dropdown",
                                        clearable=False,
                                        persistence=True,
                                        persistence_type="session",
                                        options=[
                                            {"label": x, "value": x}
                                            for x in sorted(df1_fall["Region"].unique())
                                        ],
                                        value="Sweden",
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            ]
        ),
        dcc.Graph(id="cases_graph"),
    ]
)

tab2 = html.Div(
    [
        html.H1("COVID-19 patients admitted to intensive care each week"),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            [
                                html.Label("Date"),
                                html.Label("(Day/Month/Year)"),
                                dcc.DatePickerRange(
                                    id="my-date-picker-range",  # ID to be used for callback
                                    calendar_orientation="horizontal",  # vertical or horizontal
                                    day_size=39,  # size of calendar image. Default is 39
                                    end_date_placeholder_text="Return",  # text that appears when no end date chosen
                                    with_portal=False,  # if True calendar will open in a full screen overlay portal
                                    first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                                    reopen_calendar_on_clear=True,
                                    is_RTL=False,  # True or False for direction of calendar
                                    clearable=True,  # whether or not the user can clear the dropdown
                                    number_of_months_shown=1,  # number of months shown when calendar is open
                                    min_date_allowed=df1_intense["date"].iloc[
                                        0
                                    ],  # minimum date allowed on the DatePickerRange component
                                    max_date_allowed=df1_intense["date"].iloc[-1],
                                    initial_visible_month=df1_intense["date"].iloc[-1],
                                    start_date=df1_intense["date"].iloc[0],
                                    end_date=df1_intense["date"].iloc[-1],
                                    display_format="DD MMM YY",  # how selected dates are displayed in the DatePickerRange component.
                                    month_format="MMMM, YYYY",  # how calendar headers are displayed when the calendar is opened.
                                    minimum_nights=1,  # minimum number of days between start and end date
                                    persistence=True,
                                    persisted_props=["start_date"],
                                    persistence_type="session",  # session, local, or memory. Default is 'local'
                                    updatemode="singledate",  # singledate or bothdates. Determines when callback is triggered
                                ),
                            ]
                        ),
                        html.Div(
                            html.P(
                                [
                                    html.Label(
                                        "Select County (whole of Sweden shown by default)"
                                    ),
                                    dcc.Dropdown(
                                        id="county-dropdown",
                                        clearable=False,
                                        persistence=True,
                                        persistence_type="session",
                                        options=[
                                            {"label": x, "value": x}
                                            for x in sorted(
                                                df1_intense["Region"].unique()
                                            )
                                        ],
                                        value="Sweden",
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            ]
        ),
        dcc.Graph(id="intensive_graph"),
    ]
)


app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs-example",
            value="tab-1",
            children=[
                dcc.Tab(label="Cases", value="tab-1"),
                dcc.Tab(label="Admissions to Intensive Care", value="tab-2"),
            ],
        ),
        html.Div(id="tabs-example-content"),
    ]
)


# make app callback (figure generated in update)
@app.callback(
    Output("tabs-example-content", "children"), Input("tabs-example", "value")
)
def render_content(tab):
    if tab == "tab-1":
        return tab1
    elif tab == "tab-2":
        return tab2


@app.callback(
    Output("cases_graph", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_cases_graph(value, start_date, end_date):
    mask = (df1_fall["date"] > start_date) & (df1_fall["date"] <= end_date)
    df1 = df1_fall.loc[mask]
    df = df1[(df1["Region"] == value)]
    trace1 = go.Bar(
        x=df["date"],
        y=df["Antal_fall_vecka"],
        name="Case number",
        marker_color="rgb(46,104,165)",
        hovertemplate="Date: %{x}" + "<br>Cases: %{y}",
    )

    # figure layout
    fig = go.Figure(data=trace1)
    fig.update_layout(plot_bgcolor="white", font=dict(size=12), margin=dict(r=150))
    # modify x-axis
    fig.update_xaxes(
        title="<b>Date</b>",
        showgrid=True,
        linecolor="black",
        # set start point of x-axis
        tick0="2020-01-02",
    )
    # modify y-axis
    fig.update_yaxes(
        title="<b>Number of Cases</b>",
        showgrid=True,
        gridcolor="grey",
        linecolor="black",
        # change range to envelope the appropriate range
        range=[0, max(df["Antal_fall_vecka"] + 50)],
    )

    return fig


@app.callback(
    Output("intensive_graph", "figure"),
    [
        Input("county-dropdown", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
    ],
)
def update_intensive_graph(value, start_date, end_date):
    mask1 = (df1_intense["date"] > start_date) & (df1_intense["date"] <= end_date)
    ddf1 = df1_intense.loc[mask1]
    ddf = ddf1[(ddf1["Region"] == value)]
    trace2 = go.Bar(
        x=ddf["date"],
        y=ddf["Antal_intensivvårdade_vecka"],
        name="Case number",
        marker_color="rgb(46,104,165)",
        hovertemplate="Date: %{x}" + "<br>Cases: %{y}",
    )

    # figure layout
    fig = go.Figure(data=trace2)
    fig.update_layout(plot_bgcolor="white", font=dict(size=12), margin=dict(r=150))
    # modify x-axis
    fig.update_xaxes(
        title="<b>Date</b>",
        showgrid=True,
        linecolor="black",
        # set start point of x-axis
        tick0="2020-01-02",
    )
    # modify y-axis
    fig.update_yaxes(
        title="<b>Number of Admissions to Intensive Care</b>",
        showgrid=True,
        gridcolor="grey",
        linecolor="black",
        # change range to envelope the appropriate range
        range=[0, max(ddf["Antal_intensivvårdade_vecka"] + 10)],
    )

    return fig


# server clause

app.run_server(debug=False)
