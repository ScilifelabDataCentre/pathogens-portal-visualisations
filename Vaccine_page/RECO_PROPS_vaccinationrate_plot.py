import plotly.express as px
import plotly.graph_objects as go

# import pandas as pd
import os

# from datetime import datetime as dt
from RECO_PROPS_vaccinationrate_dataprep import RECO_18plus, RECO_18to59, RECO_60plus

colours = px.colors.diverging.RdBu
colours[5] = "rgb(255,255,204)"
print(colours)


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
            line=dict(width=0.5, color="rgba(5,48,97,1)"),
            fillcolor="rgba(5,48,97,0.1)",
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
            line=dict(width=0.5, color="rgba(146,197,222,1)"),
            fillcolor="rgba(146,197,222,1)",
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
            line=dict(width=0.5, color="rgba(255,255,204,1)"),
            fillcolor="rgba(255,255,204,1)",
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
            line=dict(width=0.5, color="rgba(103,0,31,1)"),
            fillcolor="rgba(103,0,31,1)",
            stackgroup="one"  # define stack group
            # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
        )
    )
    # fig = px.area(
    #     RECO,
    #     x="date",
    #     y="Proportion",
    #     color="Dose",
    #     line_group="Dose",
    #     color_discrete_map={
    #         RECO.Dose[0]: colours[0],
    #         RECO.Dose[1]: colours[5],
    #         RECO.Dose[2]: colours[7],
    #         RECO.Dose[3]: colours[10],
    #     },
    #     hover_data={
    #         "Dose": True,
    #         "date": True,
    #         "Proportion": ":.2f",
    #     },
    # )
    fig.update_layout(
        title=" ",
        yaxis={
            "title": "",  # "<b>Percentage of Sequences Tested<br></b>",
            "ticktext": ["0", "0.2", "0.4", "0.6", "0.8", "1.0"],
            "tickvals": ["0", "0.2", "0.4", "0.6", "0.8", "1.0"],
            "range": [0, 1],
        },
        font={"size": 14},
        showlegend=False,
        hovermode="x unified",
        xaxis={
            "title": "",  # "<b><br>Date</b>",
            "tickangle": 0,
        },
        height=400,
    )
    fig.update_xaxes(type="category", ticklabelmode="period")
    fig.update_traces(hovertemplate="%{y:.2f}"),
    # fig.add_vline(
    #     x=dateline, line_width=3, line_color="darkslategrey", line_dash="dash"
    # )
    fig.show()


areagraph_func(RECO_18plus, "18plus")

# datasets = {
#     "cancer": RECO_cancer,
#     "cardio": RECO_cardio,
#     "diabetes": RECO_diabetes,
#     "respiratory": RECO_resp,
# }

# for name, df in datasets.items():
#     stacked_bar_func(df, name)
