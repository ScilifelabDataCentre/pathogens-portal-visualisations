import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime as dt
from RECOVAK_comorbidities_dataprep import (
    RECO_cancer,
    RECO_cardio,
    RECO_diabetes,
    RECO_resp,
)

map_colour = px.colors.diverging.RdBu


def stacked_bar_func(dataset, name):
    RECO = dataset
    fig = go.Figure(
        data=[
            go.Bar(
                name="Three doses",
                x=RECO.date,
                y=RECO.vacc3,
                marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
                customdata=(RECO["c19_d2"]),
                hovertemplate="%{y} <b>Tot</b>: %{customdata}",
            ),
            go.Bar(
                name="Two doses",
                x=RECO.date,
                y=RECO.vacc2,
                marker=dict(color=map_colour[8], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="One dose",
                x=RECO.date,
                y=RECO.vacc1,
                marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="Unvaccinated",
                x=RECO.date,
                y=RECO.vacc0,
                marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
                # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
                # text=RECO["c19_d2"],
                # textposition="outside",
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=18),
        margin=dict(r=250, t=0, b=0, l=0),
        width=1500,
        height=800,
        legend=dict(
            y=0.95, x=1.0, title="<b>Vaccination<br>status<br></b>", font=dict(size=22)
        ),
        showlegend=True,
        hoverlabel=dict(align="left"),
        hovermode="x unified",
    )

    # fig.add_vline(
    #     x=dt.strptime("2020-12-21", "%Y-%m-%d").timestamp() * 1000,
    #     annotation_position="top left",
    #     # fillcolor=map_colour[3],
    #     annotation_text="First doses start ",
    #     line=dict(width=2),  # , color=map_colour[3]),
    # )

    # fig.add_vline(
    #     x=dt.strptime("2021-01-04", "%Y-%m-%d").timestamp() * 1000,
    #     annotation_text=" Second doses start",
    #     line_width=2,
    # )

    # fig.add_vline(
    #     x=dt.strptime("2021-09-28", "%Y-%m-%d").timestamp() * 1000,
    #     annotation_text=" Third doses start",
    #     annotation_position="top left",
    #     line_width=2,
    # )

    # modify x-axis
    fig.update_xaxes(
        title="<br><b>Date</b>",
        showgrid=True,
        linecolor="black",
        range=["2020-01-01", max(RECO.date)],
    )

    highest_y_value = max(
        RECO["c19_d2"],
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

    # modify y-axis
    fig.update_yaxes(
        title="<b>COVID-19 cases<br></b>",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=200,
        range=[0, int(highest_y_value * 1.05)],
    )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image("Plots/comorbidity_{}.png".format(name))


# stacked_bar_func(RECO_resp, "respiratory")

datasets = {
    "cancer": RECO_cancer,
    "cardio": RECO_cardio,
    "diabetes": RECO_diabetes,
    "respiratory": RECO_resp,
}

for name, df in datasets.items():
    stacked_bar_func(df, name)
