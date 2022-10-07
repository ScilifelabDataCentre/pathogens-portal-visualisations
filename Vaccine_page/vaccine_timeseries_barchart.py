import argparse
import plotly.graph_objects as go
import pandas as pd
import os

# Import processed data
from vaccine_dataprep_Swedentots import (
    first_two_timeseries,
    third_timseries,
    fourth_timseries,
    fifth_timseries,
    Swedish_population,
)

aparser = argparse.ArgumentParser(description="Generate text insert json")
aparser.add_argument(
    "--output-dir",
    nargs="?",
    default="vaccine_plots",
    help="Output directory where the files will be saved",
)
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
# Fifth dose
fifth_timseries["Vacc_perc_population"] = (
    fifth_timseries["Antal vaccinerade"] / Swedish_population
) * 100

# separate the first and second doses
least_one_dose = first_two_timeseries[
    (first_two_timeseries["Vaccinationsstatus"] == "Minst 1 dos")
]
least_two_doses = first_two_timeseries[
    (first_two_timeseries["Vaccinationsstatus"] == "Minst 2 doser")
]

## Figure based on percentages calculated using population size

fig_pop = go.Figure()

fig_pop.add_trace(
    go.Scatter(
        x=fifth_timseries["date"],
        y=fifth_timseries["Vacc_perc_population"],
        fill="tonexty",
        # hoverinfo='x+y',
        name="At Least Five Doses",
        mode="lines",
        line=dict(width=1, color="slategrey"),
        fillcolor="slategrey",
    )
)

fig_pop.add_trace(
    go.Scatter(
        x=fourth_timseries["date"],
        y=fourth_timseries["Vacc_perc_population"],
        fill="tonexty",
        # hoverinfo='x+y',
        name="At Least Four Doses",
        mode="lines",
        line=dict(width=1, color="rgba(146,197,222,1)"),
        fillcolor="rgba(146,197,222,1)",
    )
)

fig_pop.add_trace(
    go.Scatter(
        x=third_timseries["date"],
        y=third_timseries["Vacc_perc_population"],
        fill="tonexty",
        # hoverinfo='x+y',
        name="At Least Three Doses",
        mode="lines",
        line=dict(width=1, color="rgba(255, 234, 0,1)"),
        fillcolor="rgba(255, 234, 0,1)",
    )
)

fig_pop.add_trace(
    go.Scatter(
        x=least_two_doses["date"],
        y=least_two_doses["Vacc_perc_population"],
        fill="tonexty",
        # hoverinfo='x+y',
        name="At Least Two Doses",
        mode="lines",
        line=dict(width=1, color="rgba(178,24,43,1)"),
        fillcolor="rgba(178,24,43,1)",
    )
)

fig_pop.add_trace(
    go.Scatter(
        x=least_one_dose["date"],
        y=least_one_dose["Vacc_perc_population"],
        fill="tonexty",
        # hoverinfo='x+y',
        name="At Least One Dose",
        mode="lines",
        line=dict(width=1, color="rgba(5,48,97,1)"),
        fillcolor="rgba(5,48,97,1)",
    )
)

# figure layout
fig_pop.update_layout(
    plot_bgcolor="white",
    # autosize=False,
    font=dict(size=14),
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=True,
    hovermode="x unified",
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
fig_pop.update_traces(hovertemplate="%{y:.2f}%"),
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

if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)

# make figure for web
fig_pop.write_json(
    os.path.join(args.output_dir, "vaccine_timeseries_pop_barchart.json")
)
# fig_pop.write_image("Plots/vaccine_timeseries_pop_barchart.png")
