# Produces area under the curve graphs with buttons to switch between age category data
# shows coverage for each of first 3 doses (+ no doses)
import plotly.express as px
import plotly.graph_objects as go

# import pandas as pd
import os

# from datetime import datetime as dt
from Swedishpop_vaccinecov_dataprep import RECO_18plus, RECO_18to59, RECO_60plus

# add all traces,

# def areagraph_func(dataset, name):
#     RECO = dataset
fig = go.Figure()
# traces for 18 plus age groups
fig.add_trace(
    go.Scatter(
        x=RECO_18plus["date"],
        y=RECO_18plus["four_dose"],
        # hoverinfo='x+y',
        name="Four Doses",
        mode="lines",
        line=dict(width=1, color="rgba(5,48,97,1)"),
        fillcolor="rgba(5,48,97,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_18plus["date"],
        y=RECO_18plus["three_dose"],
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
        x=RECO_18plus["date"],
        y=RECO_18plus["two_dose"],
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
        x=RECO_18plus["date"],
        y=RECO_18plus["one_dose"],
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
        x=RECO_18plus["date"],
        y=RECO_18plus["no_dose"],
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)

# traces for 18-59 age category
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["four_dose"],
        # hoverinfo='x+y',
        name="Four Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(5,48,97,1)"),
        fillcolor="rgba(5,48,97,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["three_dose"],
        # hoverinfo='x+y',
        name="Three Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["two_dose"],
        # hoverinfo='x+y',
        name="Two Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(235,235,0,1)"),
        fillcolor="rgba(235,235,0,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["one_dose"],
        # hoverinfo='x+y',
        name="One Dose",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(244,165,130,1)"),
        fillcolor="rgba(244,165,130,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["no_dose"],
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)

# traces for 60+ age category
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["four_dose"],
        # hoverinfo='x+y',
        name="Four Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(5,48,97,1)"),
        fillcolor="rgba(5,48,97,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["three_dose"],
        # hoverinfo='x+y',
        name="Three Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["two_dose"],
        # hoverinfo='x+y',
        name="Two Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(235,235,0,1)"),
        fillcolor="rgba(235,235,0,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["one_dose"],
        # hoverinfo='x+y',
        name="One Dose",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(244,165,130,1)"),
        fillcolor="rgba(244,165,130,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["no_dose"],
        # hoverinfo='x+y',
        name="No Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    )
)


fig.update_layout(
    title=" ",
    yaxis={
        "title": "<b>People with Dose Level (%)<br></b>",
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
    # width=1000,  # need to delete this when moving to json, so it can be adaptive to web
)
fig.update_layout(
    margin={"r": 0, "t": 100, "l": 0, "b": 0}, legend=dict(title="<b>Vaccine Doses</b>")
)
# fig.update_xaxes(type="category", ticklabelmode="period") #This will convert to full dates if needed
# If change above, would need to change tick angle so that dates were visible.
fig.update_traces(hovertemplate="%{y:.2f}%"),

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.25,
            yanchor="top",
            buttons=list(
                [
                    dict(
                        label="> 18",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    True,
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
                                ]
                            },
                            # {"title": "", "annotations": []},
                        ],
                    ),
                    dict(
                        label="18-59",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False,
                                    False,
                                    False,
                                ]
                            },
                            # {"title": "", "annotations": []},
                        ],
                    ),
                    dict(
                        label="> 60",
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
                                    True,
                                    True,
                                    True,
                                    True,
                                    True,
                                ]
                            },
                            # {"title": "", "annotations": []},
                        ],
                    ),
                ]
            ),
        )
    ]
)

fig.update_layout(
    annotations=[
        dict(
            text="Age Range:",
            x=-0.05,
            xref="paper",
            y=1.2,
            yref="paper",
            align="left",
            showarrow=False,
        ),
    ]
)

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")
# fig.show()
# fig.write_image("Plots/vaccination_RECO_timeseries_buttons.png")
fig.write_json("Plots/vaccination_RECO_timeseries_buttons.json")
