# Here is code related to subplots and buttons_
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import pandas as pd
from datetime import datetime as dt
import os

from comorbidity_vaccinecov_dataprep import (
    RECO_cvd_V,
    RECO_dm_V,
    RECO_resp_V,
    RECO_cancer_V,
)
from comorbidity_cases_dataprep import (
    RECO_cancer,
    RECO_cardio,
    RECO_diabetes,
    RECO_resp,
)

fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1)

# BELOW ARE TRACES FOR VACCINATION PLOT

## CVD traces for vaccination.
fig.add_trace(
    go.Scatter(
        x=RECO_cvd_V["date"],
        y=RECO_cvd_V["three_dose"],
        visible=True,
        # hoverinfo='x+y',
        name="Three Doses",
        mode="lines",
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_cvd_V["date"],
        y=RECO_cvd_V["two_dose"],
        visible=True,
        # hoverinfo='x+y',
        name="Two Doses",
        mode="lines",
        line=dict(width=1, color="rgba(235,235,0,1)"),
        fillcolor="rgba(235,235,0,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_cvd_V["date"],
        y=RECO_cvd_V["one_dose"],
        visible=True,
        # hoverinfo='x+y',
        name="One Dose",
        mode="lines",
        line=dict(width=1, color="rgba(244,165,130,1)"),
        fillcolor="rgba(244,165,130,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_cvd_V["date"],
        y=RECO_cvd_V["no_dose"],
        visible=True,
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)

# DM traces for vaccination
fig.add_trace(
    go.Scatter(
        x=RECO_dm_V["date"],
        y=RECO_dm_V["three_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="Three Doses",
        mode="lines",
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_dm_V["date"],
        y=RECO_dm_V["two_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="Two Doses",
        mode="lines",
        line=dict(width=1, color="rgba(235,235,0,1)"),
        fillcolor="rgba(235,235,0,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_dm_V["date"],
        y=RECO_dm_V["one_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="One Dose",
        mode="lines",
        line=dict(width=1, color="rgba(244,165,130,1)"),
        fillcolor="rgba(244,165,130,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_dm_V["date"],
        y=RECO_dm_V["no_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)

## RESP traces for vaccination.
fig.add_trace(
    go.Scatter(
        x=RECO_resp_V["date"],
        y=RECO_resp_V["three_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="Three Doses",
        mode="lines",
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_resp_V["date"],
        y=RECO_resp_V["two_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="Two Doses",
        mode="lines",
        line=dict(width=1, color="rgba(235,235,0,1)"),
        fillcolor="rgba(235,235,0,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_resp_V["date"],
        y=RECO_resp_V["one_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="One Dose",
        mode="lines",
        line=dict(width=1, color="rgba(244,165,130,1)"),
        fillcolor="rgba(244,165,130,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_resp_V["date"],
        y=RECO_resp_V["no_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)

# CANCER traces for vaccination
fig.add_trace(
    go.Scatter(
        x=RECO_cancer_V["date"],
        y=RECO_cancer_V["three_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="Three Doses",
        mode="lines",
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_cancer_V["date"],
        y=RECO_cancer_V["two_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="Two Doses",
        mode="lines",
        line=dict(width=1, color="rgba(235,235,0,1)"),
        fillcolor="rgba(235,235,0,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_cancer_V["date"],
        y=RECO_cancer_V["one_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="One Dose",
        mode="lines",
        line=dict(width=1, color="rgba(244,165,130,1)"),
        fillcolor="rgba(244,165,130,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_cancer_V["date"],
        y=RECO_cancer_V["no_dose"],
        visible=False,
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one",  # define stack group
        hovertemplate="%{y:.2f}%",
    ),
    1,
    1,
)

## BELOW ARE traces FOR COVID CASES (stacked barplot)

map_colour = px.colors.diverging.RdBu

# cvd traces

fig.add_trace(
    go.Bar(
        name="Three doses",
        x=RECO_cardio.date,
        y=RECO_cardio.vacc3,
        visible=True,
        marker=dict(color="rgba(146,197,222,1)", line=dict(color="#000000", width=1)),
        customdata=(RECO_cardio["c19_d2"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two doses",
        x=RECO_cardio.date,
        y=RECO_cardio.vacc2,
        visible=True,
        marker=dict(color="rgba(235,235,0,1)", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One dose",
        x=RECO_cardio.date,
        y=RECO_cardio.vacc1,
        visible=True,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Unvaccinated",
        x=RECO_cardio.date,
        y=RECO_cardio.vacc0,
        visible=True,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)

# diabetes traces
fig.add_trace(
    go.Bar(
        name="Three doses",
        x=RECO_diabetes.date,
        y=RECO_diabetes.vacc3,
        visible=False,
        marker=dict(color="rgba(146,197,222,1)", line=dict(color="#000000", width=1)),
        customdata=(RECO_diabetes["c19_d2"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two doses",
        x=RECO_diabetes.date,
        y=RECO_diabetes.vacc2,
        visible=False,
        marker=dict(color="rgba(235,235,0,1)", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One dose",
        x=RECO_diabetes.date,
        y=RECO_diabetes.vacc1,
        visible=False,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Unvaccinated",
        x=RECO_diabetes.date,
        y=RECO_diabetes.vacc0,
        visible=False,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)

# respiratory disease traces
fig.add_trace(
    go.Bar(
        name="Three doses",
        x=RECO_resp.date,
        y=RECO_resp.vacc3,
        visible=False,
        marker=dict(color="rgba(146,197,222,1)", line=dict(color="#000000", width=1)),
        customdata=(RECO_resp["c19_d2"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two doses",
        x=RECO_resp.date,
        y=RECO_resp.vacc2,
        visible=False,
        marker=dict(color="rgba(235,235,0,1)", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One dose",
        x=RECO_resp.date,
        y=RECO_resp.vacc1,
        visible=False,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Unvaccinated",
        x=RECO_resp.date,
        y=RECO_resp.vacc0,
        visible=False,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)

# cancer traces
fig.add_trace(
    go.Bar(
        name="Three doses",
        x=RECO_cancer.date,
        y=RECO_cancer.vacc3,
        visible=False,
        marker=dict(color="rgba(146,197,222,1)", line=dict(color="#000000", width=1)),
        customdata=(RECO_cancer["c19_d2"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two doses",
        x=RECO_cancer.date,
        y=RECO_cancer.vacc2,
        visible=False,
        marker=dict(color="rgba(235,235,0,1)", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One dose",
        x=RECO_cancer.date,
        y=RECO_cancer.vacc1,
        visible=False,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Unvaccinated",
        x=RECO_cancer.date,
        y=RECO_cancer.vacc0,
        visible=False,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)


# Update layout for top graph (vaccination coverage area under curve)
fig.update_layout(
    title=" ",
    yaxis={
        "title": "<b>People with Dose Level (%)<br></b>",
        "ticktext": ["0 ", "20 ", "40 ", "60 ", "80 ", "100 "],
        "tickvals": ["0", "20", "40", "60", "80", "100"],
        "range": [0, 100],
    },
    font={"size": 12},
    showlegend=False,
    hovermode="x unified",
    xaxis={
        "title": "<b>Date</b>",
        "tickangle": 0,
    },
    # height=400,
    # width=900,  # need to delete this when moving to json, so it can be adaptive to web
)

# now layout for second (bar) plot

highest_y_value = max(
    RECO_cardio["c19_d2"],
)

if highest_y_value > 10:
    yaxis_tick = 2
if highest_y_value > 20:
    yaxis_tick = 5
if highest_y_value > 50:
    yaxis_tick = 10
if highest_y_value > 100:
    yaxis_tick = 20
if highest_y_value > 150:
    yaxis_tick = 40
if highest_y_value > 500:
    yaxis_tick = 100
if highest_y_value > 1000:
    yaxis_tick = 200
if highest_y_value > 2500:
    yaxis_tick = 500


fig.update_layout(
    barmode="stack",
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=12),
    margin=dict(r=0, t=175, b=0, l=0),
    # width=1500,
    # height=800,
    # legend=dict(title="<b>Vaccine Doses</b>"),
    showlegend=False,
    hoverlabel=dict(align="left"),
    hovermode="x unified",
    xaxis2=dict(title="<b>Date</b>", showgrid=True, linecolor="black"),
    yaxis2=dict(
        title="<b>COVID-19 cases<br></b>",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=200,
        range=[0, int(highest_y_value * 1.05)],
    ),
)

# buttons

button_layer_1_height = 1.26
button_layer_2_height = 1.20
button_layer_3_height = 1.12

fig.update_layout(
    updatemenus=[
        dict(
            buttons=list(
                [
                    dict(
                        method="update",
                        args=[
                            {
                                "visible": [
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            }
                        ],
                        label="Cardiovascular Disease",
                    ),
                    dict(
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            }
                        ],
                        label="Diabetes",
                    ),
                ]
            ),
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top",
        ),
        dict(
            buttons=list(
                [
                    dict(
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            }
                        ],
                        label="Respiratory Disease",
                    ),
                    dict(
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                ]
                            }
                        ],
                        label="Cancer",
                    ),
                ]
            ),
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=button_layer_2_height,
            yanchor="top",
        ),
        dict(
            buttons=list(
                [
                    dict(
                        label="Whole time series",
                        method="relayout",
                        args=[
                            "xaxis2.range",
                            (min(RECO_cardio.date), max(RECO_cardio.date)),
                        ],
                    ),
                    dict(
                        label="Align timeline",
                        method="relayout",
                        args=[
                            "xaxis2.range",
                            ("2020-12-21", max(RECO_cvd_V.date)),
                        ],
                    ),
                ],
            ),
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=button_layer_3_height,
            yanchor="top",
        ),
    ]
)

fig.update_layout(
    annotations=[
        dict(
            text="Comorbidity:",
            x=-0.05,
            xref="paper",
            y=1.23,
            yref="paper",
            align="left",
            showarrow=False,
        ),
        dict(
            text="Timeframe:",
            x=-0.05,
            xref="paper",
            y=1.09,
            yref="paper",
            showarrow=False,
        ),
    ]
)


if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")
# fig.show()
fig.write_json("Plots/comorbs_subplot_button.json")
