import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Import processed data
from vaccine_dataprep_Swedentots import (
    df_vacc,
    third_vacc_dose,
    Swedish_population,
)

# calculate percentages based on population size
df_vacc["Vacc_perc_population"] = (
    df_vacc["Antal vaccinerade"] / Swedish_population
) * 100

# print(df_vacc.head())
least_one_dose = df_vacc[(df_vacc["Vaccinationsstatus"] == "Minst 1 dos")]
least_two_doses = df_vacc[(df_vacc["Vaccinationsstatus"] == "Minst 2 doser")]

trace1 = go.Bar(
    x=least_one_dose["date"],
    y=least_one_dose["Procent vaccinerade"],
    name="At Least One Dose Received",
    marker_color="rgb(5,48,97)",
    hovertemplate="Date: %{x}" + "<br>Percent One Dose: %{y:.2f}%",
)
trace2 = go.Bar(
    x=least_two_doses["date"],
    y=least_two_doses["Procent vaccinerade"],
    name="At Least Two Doses Received",
    marker_color="rgb(178,24,43)",
    marker_pattern_shape="/",
    hovertemplate="Date: %{x}" + "<br>Percent Full Dose: %{y:.2f}%",
)

# figure layout
fig = go.Figure(data=[trace1, trace2])
fig.update_layout(
    plot_bgcolor="white",
    font=dict(size=14),
    margin=dict(l=0, r=50, t=0, b=0),
    showlegend=True,
    legend=dict(
        title=" ",
        orientation="h",
        # yanchor="bottom",
        y=1.2,
        # xanchor="right",
        # x=0.5,
        font=dict(size=14),
    ),
)
# modify x-axis
fig.update_xaxes(
    title="<b>Date</b>",
    showgrid=True,
    linecolor="black",
    # set start point of x-axis
    tick0=least_one_dose["date"].iloc[0],
)
# modify y-axis
fig.update_yaxes(
    title="<b>Percentage Vaccinated</b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # change range to envelope the appropriate range
    range=[0, 100],
)

# fig.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

fig.write_json("Plots/vaccine_timeseries_barchart.json")
fig.write_image("Plots/vaccine_timeseries_barchart.png")


## Figure based on percentages calculated using population size

trace3 = go.Bar(
    x=least_one_dose["date"],
    y=least_one_dose["Vacc_perc_population"],
    name="At Least One Dose Received",
    marker_color="rgb(5,48,97)",
    hovertemplate="Date: %{x}" + "<br>Percent One Dose: %{y:.2f}%",
)
trace4 = go.Bar(
    x=least_two_doses["date"],
    y=least_two_doses["Vacc_perc_population"],
    name="At Least Two Doses Received",
    marker_color="rgb(178,24,43)",
    marker_pattern_shape="/",
    hovertemplate="Date: %{x}" + "<br>Percent Full Dose: %{y:.2f}%",
)

# figure layout
fig_pop = go.Figure(data=[trace3, trace4])
fig_pop.update_layout(
    plot_bgcolor="white",
    font=dict(size=14),
    margin=dict(l=0, r=50, t=0, b=0),
    showlegend=True,
    legend=dict(
        title=" ",
        orientation="h",
        # yanchor="bottom",
        y=1.2,
        # xanchor="right",
        # x=0.5,
        font=dict(size=14),
    ),
)
# modify x-axis
fig_pop.update_xaxes(
    title="<b>Date</b>",
    showgrid=True,
    linecolor="black",
    # set start point of x-axis
    tick0=least_one_dose["date"].iloc[0],
)
# modify y-axis
fig_pop.update_yaxes(
    title="<b>Percentage Vaccinated</b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # change range to envelope the appropriate range
    range=[0, 100],
)

# fig_pop.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

fig_pop.write_json("Plots/vaccine_timeseries_pop_barchart.json")
fig_pop.write_image("Plots/vaccine_timeseries_pop_barchart.png")
