# Produces individual area under the curve graphs for data for each condition
# shows different doses
import plotly.express as px
import plotly.graph_objects as go

# import pandas as pd
import os

# from datetime import datetime as dt
from RECO_comorbs_vaccrate_dataprep import (
    RECO_cvd_V,
    RECO_dm_V,
    RECO_resp_V,
    RECO_cancer_V,
)


def areagraph_func(dataset, name):
    RECO = dataset
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=RECO["date"],
            y=RECO["three_dose"],
            # hoverinfo='x+y',
            name="Three Doses",
            mode="lines",
            line=dict(width=1, color="rgba(146,197,222,1)"),
            fillcolor="rgba(146,197,222,1)",
            stackgroup="one"  # define stack group
            # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=RECO["date"],
            y=RECO["two_dose"],
            # hoverinfo='x+y',
            name="Two Doses",
            mode="lines",
            line=dict(width=1, color="rgba(235,235,0,1)"),
            fillcolor="rgba(235,235,0,1)",
            stackgroup="one"  # define stack group
            # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=RECO["date"],
            y=RECO["one_dose"],
            # hoverinfo='x+y',
            name="One Dose",
            mode="lines",
            line=dict(width=1, color="rgba(244,165,130,1)"),
            fillcolor="rgba(244,165,130,1)",
            stackgroup="one"  # define stack group
            # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=RECO["date"],
            y=RECO["no_dose"],
            # hoverinfo='x+y',
            name="No Doses",
            mode="lines",
            line=dict(width=1, color="rgba(178,24,43,1)"),
            fillcolor="rgba(178,24,43,1)",
            stackgroup="one"  # define stack group
            # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
        )
    )

    fig.update_layout(
        title=" ",
        yaxis={
            "title": "<b>Percentage of People with Dose Level<br></b>",
            "ticktext": ["0 ", "20 ", "40 ", "60 ", "80 ", "100 "],
            "tickvals": ["0", "20", "40", "60", "80", "100"],
            "range": [0, 100],
        },
        font={"size": 12},
        showlegend=True,
        hovermode="x unified",
        xaxis={
            "title": "<b><br>Date</b>",
            "tickangle": 0,
        },
        # height=400,
        width=900,  # need to delete this when moving to json, so it can be adaptive to web
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.update_xaxes(type="category", ticklabelmode="period") #This will convert to full dates if needed
    # If change above, would need to change tick angle so that dates were visible.
    fig.update_traces(hovertemplate="%{y:.2f}%"),
    # fig.add_vline(
    #     x=dateline, line_width=3, line_color="darkslategrey", line_dash="dash"
    # )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image(
        "Plots/vaccination_RECO_comorbs_{}.png".format(name)
    )  # needs to write json and be .json


# run all graphs
datasets = {
    "CVD": RECO_cvd_V,
    "DM": RECO_dm_V,
    "resp": RECO_resp_V,
    "cancer": RECO_cancer_V,
}

for name, df in datasets.items():
    areagraph_func(df, name)
