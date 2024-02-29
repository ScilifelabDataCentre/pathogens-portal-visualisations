# Here is code related to subplots and buttons
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Swedishpop_vaccinecov_dataprep import RECO_18plus, RECO_18to59, RECO_60plus
from Swedishpop_ICU_dataprep import RECO_icu_18plus, RECO_icu_18to59, RECO_icu_60plus

# Function to determine which part ofgrapghs to show
def get_xaxis(x1, x2):
    r_start = max(min(x1), min(x2))
    r_end = min(max(x1), max(x2))
    x_axes = {
        "xaxis": {
            "all": dict(title="<b>Date</b>", range=[min(x1), max(x1)], anchor="y"),
            "align": dict(title="<b>Date</b>", range=[r_start, r_end], anchor="y"),
        },
        "xaxis2": {
            "all": dict(
                title="<b>Date</b>",
                showgrid=True,
                linecolor="black",
                range=[min(x2), max(x2)],
                anchor="y2",
            ),
            "align": dict(
                title="<b>Date</b>",
                showgrid=True,
                linecolor="black",
                range=[r_start, r_end],
                anchor="y2",
            ),
        },
    }
    return x_axes


fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1)

# BELOW TRACES FOR SCATTER PLOT

# traces for 18 plus age groups
fig.add_trace(
    go.Scatter(
        x=RECO_18plus["date"],
        y=RECO_18plus["six_dose"],
        # hoverinfo='x+y',
        name="Six Doses",
        mode="lines",
        line=dict(width=1, color="grey"),
        fillcolor="grey",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_18plus["date"],
        y=RECO_18plus["five_dose"],
        # hoverinfo='x+y',
        name="Five Doses",
        mode="lines",
        line=dict(width=1, color="black"),
        fillcolor="black",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    ),
    1,
    1,
)
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
)

# traces for 18-59 age category
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["six_dose"],
        # hoverinfo='x+y',
        name="Six Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="grey"),
        fillcolor="grey",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_18to59["date"],
        y=RECO_18to59["five_dose"],
        # hoverinfo='x+y',
        name="Five Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="black"),
        fillcolor="black",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    ),
    1,
    1,
)
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
)

# traces for 60+ age category
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["six_dose"],
        # hoverinfo='x+y',
        name="Six Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="grey"),
        fillcolor="grey",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    ),
    1,
    1,
)
fig.add_trace(
    go.Scatter(
        x=RECO_60plus["date"],
        y=RECO_60plus["five_dose"],
        # hoverinfo='x+y',
        name="Five Doses",
        mode="lines",
        visible=False,
        line=dict(width=1, color="black"),
        fillcolor="black",
        stackgroup="one"  # define stack group
        # hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
    ),
    1,
    1,
)
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
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
    ),
    1,
    1,
)

# BELOW ARE THE BAR PLOT TRACES

map_colour = px.colors.diverging.RdBu
map_colour[5] = "rgb(235, 235, 0)"

# traces for 18 plus age groups
fig.add_trace(
    go.Bar(
        name="Six Doses",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc6,
        marker=dict(color="grey", line=dict(color="#000000", width=1)),
        customdata=(RECO_icu_18plus["c19_i1"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Five Doses",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc5,
        marker=dict(color="black", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Four Doses",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc4,
        marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Three Doses",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc3,
        marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two Doses",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc2,
        marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One Dose",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc1,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="No doses",
        x=RECO_icu_18plus.date,
        y=RECO_icu_18plus.vacc0,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
        # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
        # text=RECO_intense["c19_i1"],
        # textposition="outside",
    ),
    2,
    1,
)
# traces for 18-59 age groups
fig.add_trace(
    go.Bar(
        name="Six Doses",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc6,
        visible=False,
        marker=dict(color="grey", line=dict(color="#000000", width=1)),
        customdata=(RECO_icu_18to59["c19_i1"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Five Doses",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc5,
        visible=False,
        marker=dict(color="black", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Four Doses",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc4,
        visible=False,
        marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Three Doses",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc3,
        visible=False,
        marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two Doses",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc2,
        visible=False,
        marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One Dose",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc1,
        visible=False,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="No Doses",
        x=RECO_icu_18to59.date,
        y=RECO_icu_18to59.vacc0,
        visible=False,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
        # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
        # text=RECO_intense["c19_i1"],
        # textposition="outside",
    ),
    2,
    1,
)
# traces for 60 plus age groups
fig.add_trace(
    go.Bar(
        name="Six Doses",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc6,
        visible=False,
        marker=dict(color="grey", line=dict(color="#000000", width=1)),
        customdata=(RECO_icu_60plus["c19_i1"]),
        hovertemplate="%{y} <b>Tot</b>: %{customdata}",
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Five Doses",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc5,
        visible=False,
        marker=dict(color="black", line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Four Doses",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc4,
        visible=False,
        marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Three Doses",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc3,
        visible=False,
        marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="Two Doses",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc2,
        visible=False,
        marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="One Dose",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc1,
        visible=False,
        marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
    ),
    2,
    1,
)
fig.add_trace(
    go.Bar(
        name="No Doses",
        x=RECO_icu_60plus.date,
        y=RECO_icu_60plus.vacc0,
        visible=False,
        marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
        # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
        # text=RECO_intense["c19_i1"],
        # textposition="outside",
    ),
    2,
    1,
)

# Get appropriate range for x axes
x_axes = get_xaxis(x1=RECO_18plus.date, x2=RECO_icu_18plus.date)

# Update layout for top graph

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
    xaxis=x_axes["xaxis"]["all"],
    # height=400,
    # width=1000,  # need to delete this when moving to json, so it can be adaptive to web
)

# now layout for second (bar) plot

highest_y_value = max(
    RECO_icu_18plus["c19_i1"],
)

fig.update_layout(
    barmode="stack",
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=12),
    margin=dict(r=0, t=150, b=0, l=0),
    # width=1500,
    # height=800,
    # legend=dict(title="<b>Vaccine Doses</b>"),
    showlegend=False,
    hoverlabel=dict(align="left"),
    hovermode="x unified",
    xaxis2=x_axes["xaxis2"]["all"],
    yaxis2=dict(
        title="<b>Admissions to ICU<br></b>",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=50,
        range=[0, int(highest_y_value * 1.05)],
    ),
)

# Buttons

button_layer_1_height = 1.20
button_layer_2_height = 1.12

fig.update_layout(
    updatemenus=[
        dict(
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
                                    False,
                                    False,
                                ]
                            },
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
                                    False,
                                    False,
                                    True,
                                    True,
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
                                ]
                            },
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
                                    False,
                                    False,
                                    False,
                                    False,
                                    True,
                                    True,
                                    True,
                                    True,
                                    True,
                                    True,
                                    True,
                                ]
                            },
                        ],
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
                        label="Show all data",
                        method="relayout",
                        args=[
                            {
                                "xaxis": x_axes["xaxis"]["all"],
                                "xaxis2": x_axes["xaxis2"]["all"],
                            }
                        ],
                    ),
                    dict(
                        label="Align timeline",
                        method="relayout",
                        args=[
                            {
                                "xaxis": x_axes["xaxis"]["align"],
                                "xaxis2": x_axes["xaxis2"]["align"],
                            }
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
            y=button_layer_2_height,
            yanchor="top",
        ),
    ]
)

fig.update_layout(
    annotations=[
        dict(
            text="Age Range:",
            x=-0.03,
            xref="paper",
            y=button_layer_1_height * 0.978,
            yref="paper",
            align="left",
            showarrow=False,
        ),
        dict(
            text="Timeframe:",
            x=-0.03,
            xref="paper",
            y=button_layer_2_height * 0.978,
            yref="paper",
            showarrow=False,
        ),
    ]
)

fig.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")
fig.write_json("Plots/swedishpop_subplot_button.json")
