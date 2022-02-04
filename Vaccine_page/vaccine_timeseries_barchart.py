import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Import processed data
from vaccine_dataprep_Swedentots import (
    df_vacc,
    third_timseries,
    Swedish_population,
)

# calculate percentages based on population size
# first and second doses
df_vacc["Vacc_perc_population"] = (
    df_vacc["Antal vaccinerade"] / Swedish_population
) * 100
# Third dose
third_timseries["Vacc_perc_population"] = (
    third_timseries["Antal vaccinerade"] / Swedish_population
) * 100

# separate the first and second doses
least_one_dose = df_vacc[(df_vacc["Vaccinationsstatus"] == "Minst 1 dos")]
least_two_doses = df_vacc[(df_vacc["Vaccinationsstatus"] == "Minst 2 doser")]

## Figure based on percentages calculated using population size

trace1 = go.Bar(
    x=least_one_dose["date"],
    y=least_one_dose["Vacc_perc_population"],
    name="At Least One Dose",
    marker_color="rgb(5,48,97)",
    marker_line_color="black",
    hovertemplate="Number of Doses: One Dose"
    + "<br>Date: %{x}"
    + "<br>Percent Vaccinated: %{y:.2f}%<extra></extra>",
)
trace2 = go.Bar(
    x=least_two_doses["date"],
    y=least_two_doses["Vacc_perc_population"],
    name="At Least Two Doses",
    marker_color="rgb(178,24,43)",
    marker_line_color="black",
    hovertemplate="Number of Doses: Two Doses"
    + "<br>Date: %{x}"
    + "<br>Percent Vaccinated: %{y:.2f}%<extra></extra>",
)
trace3 = go.Bar(
    x=third_timseries["date"],
    y=third_timseries["Vacc_perc_population"],
    name="At Least Three Doses",
    marker_color="rgb(255, 234, 0)",
    marker_line_color="black",
    hovertemplate="Number of Doses: Three Doses"
    + "<br>Date: %{x}"
    + "<br>Percent Vaccinated: %{y:.2f}%<extra></extra>",
)

# figure layout
fig_pop = go.Figure(data=[trace1, trace2, trace3])
fig_pop.update_layout(
    plot_bgcolor="white",
    font=dict(size=14),
    margin=dict(l=0, r=50, t=0, b=0),
    showlegend=True,
    legend=dict(
        title=" ",
        orientation="h",
        # yanchor="bottom",
        y=1.15,
        # xanchor="right",
        # x=0.2,
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
    range=[0, 100],
)

# fig_pop.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

# we only currently use this map
fig_pop.write_json("Plots/vaccine_timeseries_pop_barchart.json")
