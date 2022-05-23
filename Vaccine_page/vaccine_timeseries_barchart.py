import argparse
import plotly.graph_objects as go
import pandas as pd
import os

# Import processed data
from vaccine_dataprep_Swedentots import (
    first_two_timeseries,
    third_timseries,
    fourth_timseries,
    Swedish_population,
)

aparser = argparse.ArgumentParser(description="Generate text insert json")
aparser.add_argument("--output-dir", nargs="?", default="vaccine_plots",
                     help="Output directory where the files will be saved")
args = aparser.parse_args()

# calculate percentages based on population size
# first and second doses
first_two_timeseries["Vacc_perc_population"] = (
    first_two_timeseries["Antal vaccinerade"] / Swedish_population
) * 100
# Third dose
third_timseries["Vacc_perc_population"] = (
    third_timseries["Antal vaccinerade"] / Swedish_population
) * 100
# Fourth dose
fourth_timseries["Vacc_perc_population"] = (
    fourth_timseries["Antal vaccinerade"] / Swedish_population
) * 100

# separate the first and second doses
least_one_dose = first_two_timeseries[(first_two_timeseries["Vaccinationsstatus"] == "Minst 1 dos")]
least_two_doses = first_two_timeseries[(first_two_timeseries["Vaccinationsstatus"] == "Minst 2 doser")]

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
trace4 = go.Bar(
    x=fourth_timseries["date"],
    y=fourth_timseries["Vacc_perc_population"],
    name="At Least Four Doses",
    marker_color="rgb(146,197,222)",
    marker_line_color="black",
    hovertemplate="Number of Doses: Four Doses"
    + "<br>Date: %{x}"
    + "<br>Percent Vaccinated: %{y:.2f}%<extra></extra>",
)

# figure layout
fig_pop = go.Figure(data=[trace1, trace2, trace3, trace4])
fig_pop.update_layout(
    plot_bgcolor="white",
    font=dict(size=14),
    margin=dict(l=0, r=50, t=0, b=0),
    showlegend=True,
    legend=dict(
        title=" ",
        # orientation="h",
        # yanchor="bottom",
        y=1.15,
        # xanchor="right",
        x=0.05,
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

if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)

# make figure for web
fig_pop.write_json(os.path.join(args.output_dir, "vaccine_timeseries_pop_barchart.json"))
# fig_pop.write_image("Plots/vaccine_timeseries_pop_barchart.png")
