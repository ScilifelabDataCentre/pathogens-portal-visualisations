# Will create indicators and bar chart to display on page (can break script down if components are needed separately)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# from datetime import datetime as dt
# from datetime import timedelta

# Import processed data
from vaccine_dataprep_Swedentots import (
    df_vacc,
    # df_vacc_ålders, (if switch to age data. No date and not possible to figure out date!!)
    third_vacc_dose,
    Swedish_population,
)

## Import and sort data from Folkhälsomyndigheten USE THEIR PERCENTAGE CALCULATIONS FIRST!
## initially deal with data from first two doses
# df_vacc = df_vacc_ålders (use this if we switch to ålders and get rid of date)

one_dose_swe = df_vacc[
    (df_vacc["date"] == df_vacc["date"].max())
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

# print(one_dose_swe)
one_dose_swe = float(one_dose_swe["Procent vaccinerade"].round(2))

one_dose_lastweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-2])
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

# print(one_dose_lastweek)
one_dose_lastweek = float(one_dose_lastweek["Procent vaccinerade"].round(2))

one_dose_twoweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-3])
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

# print(one_dose_twoweek)
one_dose_twoweek = float(one_dose_twoweek["Procent vaccinerade"].round(2))

least_two_dose_swe = df_vacc[
    (df_vacc["date"] == df_vacc["date"].max())
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

# print(least_two_dose_swe)
least_two_dose_swe = float(least_two_dose_swe["Procent vaccinerade"].round(2))

least_two_dose_lastweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-2])
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

# print(least_two_dose_lastweek)
least_two_dose_lastweek = float(least_two_dose_lastweek["Procent vaccinerade"].round(2))

least_two_dose_twoweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-3])
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

# print(least_two_dose_twoweek)
least_two_dose_twoweek = float(least_two_dose_twoweek["Procent vaccinerade"].round(2))

## Now work out rates
rate_onedose_lastwk = float("{:.2f}".format(one_dose_swe - one_dose_lastweek))
rate_onedose_twowk = float("{:.2f}".format(one_dose_lastweek - one_dose_twoweek))
rate_leasttwodose_lastwk = float(
    "{:.2f}".format(least_two_dose_swe - least_two_dose_lastweek)
)
rate_leasttwodose_twowk = float(
    "{:.2f}".format(least_two_dose_lastweek - least_two_dose_twoweek)
)

## Now data for 3rd dose from FoHM (not currently included in time series)
## may need to note that 'at least 2 doses COULD include 3rd dose'...

# only have total number for now, so no rate calculations etc. for now
third_vacc_dose_tot = third_vacc_dose[(third_vacc_dose["Åldersgrupp"] == "Totalt")]

third_vacc_dose_tot = float(third_vacc_dose_tot["Procent vaccinerade"].round(2))
# print(third_vacc_dose_tot)

## Everything above deals with percentages given by FoHM.
## Now need to calculate percentages based on whole population of Sweden

# Calculate percentage of population (rather than FoHM percentages)

df_vacc["Vacc_perc_population"] = (
    df_vacc["Antal vaccinerade"] / Swedish_population
) * 100

one_dose_pop = df_vacc[
    (df_vacc["date"] == df_vacc["date"].max())
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

one_dose_pop = float(one_dose_pop["Vacc_perc_population"].round(2))
# print(one_dose_pop)

one_dose_pop_lastweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-2])
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

one_dose_pop_lastweek = float(one_dose_pop_lastweek["Vacc_perc_population"].round(2))
# print(one_dose_pop_lastweek)

one_dose_pop_twoweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-3])
    & (df_vacc["Vaccinationsstatus"] == "Minst 1 dos")
]

one_dose_pop_twoweek = float(one_dose_pop_twoweek["Vacc_perc_population"].round(2))
# print(one_dose_pop_twoweek)

least_two_dose_pop = df_vacc[
    (df_vacc["date"] == df_vacc["date"].max())
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

least_two_dose_pop = float(least_two_dose_pop["Vacc_perc_population"].round(2))
# print(least_two_dose_pop)

least_two_dose_pop_lastweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-2])
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

least_two_dose_pop_lastweek = float(
    least_two_dose_pop_lastweek["Vacc_perc_population"].round(2)
)
# print(least_two_dose_pop_lastweek)

least_two_dose_pop_twoweek = df_vacc[
    (df_vacc["date"] == df_vacc["date"].unique()[-3])
    & (df_vacc["Vaccinationsstatus"] == "Minst 2 doser")
]

least_two_dose_pop_twoweek = float(
    least_two_dose_pop_twoweek["Vacc_perc_population"].round(2)
)
# print(least_two_dose_pop_twoweek)

## Now work out rates
rate_onedose_pop_lastwk = float("{:.2f}".format(one_dose_pop - one_dose_pop_lastweek))
rate_onedose_pop_twowk = float(
    "{:.2f}".format(one_dose_pop_lastweek - one_dose_pop_twoweek)
)
rate_leasttwodose_pop_lastwk = float(
    "{:.2f}".format(least_two_dose_pop - least_two_dose_pop_lastweek)
)
rate_leasttwodose_pop_twowk = float(
    "{:.2f}".format(least_two_dose_pop_lastweek - least_two_dose_pop_twoweek)
)

# now look at 3rd dose (will not have rate data in this case)

third_vacc_dose["Vacc_perc_population"] = (
    third_vacc_dose["Antal vaccinerade"] / Swedish_population
) * 100

third_vacc_dose_pop = third_vacc_dose[
    (third_vacc_dose["Åldersgrupp"] == "Totalt")
    & (third_vacc_dose["Region"] == "Sweden")
]

third_vacc_dose_pop = float(third_vacc_dose_pop["Vacc_perc_population"].round(2))
# print(third_vacc_dose_pop)

###### Gathering all the values that we'll need to display HERE (so we can insert them in the html)!!

## The % (FoHM) given one dose in total
one_dose_swe
## The % (FoHM) given two doses in total
least_two_dose_swe
## The % (FoHM) given three doses in total
third_vacc_dose_tot
## The % (FoHM) given one dose last week
rate_onedose_lastwk
## The % (FoHM) given two doses last week
rate_leasttwodose_lastwk
## The change in vaccination rate for one dose (FoHM) between latest 2 weeks
onedose_ratechange = rate_onedose_lastwk - rate_onedose_twowk
## The change in vaccination rate for two doses (FoHM) between latest 2 weeks
twodose_ratechange = rate_leasttwodose_lastwk - rate_leasttwodose_twowk
## The % (whole population) given one dose in total
one_dose_pop
## The % (whole population) given two doses in total
least_two_dose_pop
## The % (whole population) given three doses in total
third_vacc_dose_pop
## The % (whole population) given one dose last week
one_dose_pop_lastweek
## The % (whole population) given two doses last week
least_two_dose_pop_lastweek
## The change in vaccination rate for one dose (whole population) between latest 2 weeks
onedose_ratechange_pop = rate_onedose_pop_lastwk - rate_onedose_pop_twowk
## The change in vaccination rate for two doses (whole population) between latest 2 weeks
twodose_ratechange_pop = rate_leasttwodose_pop_lastwk - rate_leasttwodose_pop_twowk

# Now will make a dataframe so that we can create a grouped bar chart as a summary

vaccine_dose_totals = pd.DataFrame()
vaccine_dose_totals["Doses"] = ["1 dose", "2 doses", "3 doses"]
vaccine_dose_totals["FOHM_perc"] = [
    one_dose_swe,
    least_two_dose_swe,
    third_vacc_dose_tot,
]
vaccine_dose_totals["POP_perc"] = [
    one_dose_pop,
    least_two_dose_pop,
    third_vacc_dose_pop,
]

# initiate barchart

trace1 = go.Bar(
    x=vaccine_dose_totals["Doses"],
    y=vaccine_dose_totals["FOHM_perc"],
    name="FoHM Data",
    marker_color="rgb(5,48,97)",
    hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
)
trace2 = go.Bar(
    x=vaccine_dose_totals["Doses"],
    y=vaccine_dose_totals["POP_perc"],
    name="Population Data",
    marker_color="rgb(178,24,43)",
    # marker_pattern_shape="/",
    hovertemplate="Number of Doses: %{x}" + "<br>Percent Receiving the Dose: %{y:.2f}%",
)

# figure layout
fig = go.Figure(data=[trace1, trace2])
fig.update_layout(
    plot_bgcolor="white",
    font=dict(size=16),
    margin=dict(l=0, r=50, t=0, b=0),
    showlegend=True,
    legend=dict(
        title=" ",
        orientation="h",
        # yanchor="bottom",
        y=1.2,
        # xanchor="right",
        # x=0.5,
        font=dict(size=16),
    ),
)
# modify x-axis
fig.update_xaxes(
    title="<b>Number of Doses Received</b>",
    showgrid=True,
    linecolor="black",
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

fig.show()

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")

fig.write_json("Plots/Total_vaccinated_barchart.json")
# png displays strangely (because I haven't set sizes - will be determined in html)
fig.write_image("Plots/Total_vaccinated_barchart.png")

# # this figure should not ultimately be included - use the app code in html to insert the values we want (all above!)
# # this figure shows some numbers relevant to FoHM calculations
# Vacc_doses_fohm = go.Figure(
#     go.Indicator(
#         mode="number",  # add + delta to just show how much more % was vaccinated (would need to delete rate delta)
#         value=one_dose_swe,
#         title={
#             "text": "<b>Percentage Population Given Single Vaccine Dose<br> and Change in Rate Compared to Previous Week</b>"
#         },
#         delta={
#             "reference": one_dose_lastweek,
#             "relative": False,
#             "position": "right",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0, 1], "y": [0, 0.35]},
#     )
# )
# Vacc_doses_fohm.add_trace(
#     go.Indicator(
#         mode="number",  # add + delta to just show how much more % was vaccinated (would need to delete rate delta)
#         value=least_two_dose_swe,
#         title={
#             "text": "<b>Percentage Population Given Two Doses<br> and Change in Rate Compared to Previous Week</b>"
#         },
#         delta={
#             "reference": least_two_dose_lastweek,
#             "relative": False,
#             "position": "right",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0, 1], "y": [0.65, 1]},
#     )
# )
# Vacc_doses_fohm.add_trace(
#     go.Indicator(
#         mode="delta",
#         value=rate_onedose_lastwk,
#         title={"text": " "},
#         delta={
#             "reference": rate_onedose_twowk,
#             "relative": False,
#             "position": "right",
#             "decreasing.color": "red",
#             "increasing.color": "green",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0.75, 1], "y": [0.65, 1]},
#     )
# )
# Vacc_doses_fohm.add_trace(
#     go.Indicator(
#         mode="delta",
#         value=rate_leasttwodose_lastwk,
#         title={"text": " "},
#         delta={
#             "reference": rate_leasttwodose_twowk,
#             "relative": False,
#             "position": "right",
#             "decreasing.color": "red",
#             "increasing.color": "green",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0.75, 1], "y": [0, 0.35]},
#     )
# )

# # This is just to see the indicators
# Vacc_doses_fohm.show()

# # this figure should not ultimately be included - use the app code in html to insert the values we want (all above!)
# # this figure shows some numbers relevant to population level calculations
# Vacc_doses_pop = go.Figure(
#     go.Indicator(
#         mode="number",  # add + delta to just show how much more % was vaccinated (would need to delete rate delta)
#         value=one_dose_pop,
#         title={
#             "text": "<b>Percentage Population Given Single Vaccine Dose<br> and Change in Rate Compared to Previous Week</b>"
#         },
#         delta={
#             "reference": one_dose_pop_lastweek,
#             "relative": False,
#             "position": "right",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0, 1], "y": [0, 0.35]},
#     )
# )
# Vacc_doses_pop.add_trace(
#     go.Indicator(
#         mode="number",  # add + delta to just show how much more % was vaccinated (would need to delete rate delta)
#         value=least_two_dose_pop,
#         title={
#             "text": "<b>Percentage Population Given Two Doses<br> and Change in Rate Compared to Previous Week</b>"
#         },
#         delta={
#             "reference": least_two_dose_pop_lastweek,
#             "relative": False,
#             "position": "right",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0, 1], "y": [0.65, 1]},
#     )
# )
# Vacc_doses_pop.add_trace(
#     go.Indicator(
#         mode="delta",
#         value=rate_onedose_pop_lastwk,
#         title={"text": " "},
#         delta={
#             "reference": rate_onedose_pop_twowk,
#             "relative": False,
#             "position": "right",
#             "decreasing.color": "red",
#             "increasing.color": "green",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0.75, 1], "y": [0.65, 1]},
#     )
# )
# Vacc_doses_pop.add_trace(
#     go.Indicator(
#         mode="delta",
#         value=rate_leasttwodose_pop_lastwk,
#         title={"text": " "},
#         delta={
#             "reference": rate_leasttwodose_pop_twowk,
#             "relative": False,
#             "position": "right",
#             "decreasing.color": "red",
#             "increasing.color": "green",
#         },
#         number={"font": {"size": 70}},
#         domain={"x": [0.75, 1], "y": [0, 0.35]},
#     )
# )

# # This is just to see the indicators
# Vacc_doses_pop.show()
