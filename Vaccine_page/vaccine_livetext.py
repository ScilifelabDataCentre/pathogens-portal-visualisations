# Will create indicators to display on page
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import json

# Import processed data
from vaccine_dataprep_Swedentots import (
    df_vacc,
    # third_vacc_dose,
    third_timseries,
    fourth_vacc_dose,
    Swedish_population,
)

## Import and sort data from Folkhälsomyndigheten USE THEIR PERCENTAGE CALCULATIONS FIRST!
## initially deal with data from first two doses

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

## Now data for 3rd dose (given new time series data Jan 2022)

third_dose_swe = third_timseries[
    (third_timseries["date"] == third_timseries["date"].max())
]

third_dose_swe = float(third_dose_swe["Procent vaccinerade"].round(2))


third_dose_lastweek = third_timseries[
    (third_timseries["date"] == third_timseries["date"].unique()[-2])
]

third_dose_lastweek = float(third_dose_lastweek["Procent vaccinerade"].round(2))

third_dose_twoweek = third_timseries[
    (third_timseries["date"] == third_timseries["date"].unique()[-3])
]

third_dose_twoweek = float(third_dose_twoweek["Procent vaccinerade"].round(2))

# Now figure out rates

rate_threedose_lastwk = float("{:.2f}".format(third_dose_swe - third_dose_lastweek))
rate_threedose_twowk = float("{:.2f}".format(third_dose_lastweek - third_dose_twoweek))

# Data on fourth doses (no timeseries data as of March 2022)

fourth_vacc_dose = fourth_vacc_dose[(fourth_vacc_dose["Åldersgrupp"] == "Totalt")]
fourth_dose_swe = float(fourth_vacc_dose["Procent vaccinerade"].round(2))

## Everything above deals with percentages based on the percantage eiligible to take the vaccine
## Now need to calculate percentages based on whole population of Sweden

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

# now look at 3rd dose (rate data become available Late Jan 2022)

# print(third_timseries.head())

third_timseries["Vacc_perc_population"] = (
    third_timseries["Antal vaccinerade"] / Swedish_population
) * 100

third_vacc_dose_pop = third_timseries[
    (third_timseries["date"] == third_timseries["date"].max())
]

third_vacc_dose_pop = float(third_vacc_dose_pop["Vacc_perc_population"].round(2))

third_dose_pop_lastweek = third_timseries[
    (third_timseries["date"] == third_timseries["date"].unique()[-2])
]

third_dose_pop_lastweek = float(
    third_dose_pop_lastweek["Vacc_perc_population"].round(2)
)

third_dose_pop_twoweek = third_timseries[
    (third_timseries["date"] == third_timseries["date"].unique()[-3])
]

third_dose_pop_twoweek = float(third_dose_pop_twoweek["Vacc_perc_population"].round(2))

# Now figure out rates

rate_threedose_pop_lastwk = float(
    "{:.2f}".format(third_vacc_dose_pop - third_dose_pop_lastweek)
)
rate_threedose_pop_twowk = float(
    "{:.2f}".format(third_dose_pop_lastweek - third_dose_pop_twoweek)
)

# Data for fourth dose

fourth_vacc_dose["Vacc_perc_population"] = (
    fourth_vacc_dose["Antal vaccinerade"] / Swedish_population
) * 100

fourth_dose_pop = float(fourth_vacc_dose["Vacc_perc_population"].round(2))

## calculate differences in rates (no rate available for fourth dose)

## The change in vaccination rate for one dose for the eligible population between latest 2 weeks

onedose_ratechange = float("{:.2f}".format(rate_onedose_lastwk - rate_onedose_twowk))

## The change in vaccination rate for two doses for the eligible population between latest 2 weeks

twodose_ratechange = float(
    "{:.2f}".format(rate_leasttwodose_lastwk - rate_leasttwodose_twowk)
)

## The change in vaccination rate for three doses for the eligible population between latest 2 weeks

threedose_ratechange = float(
    "{:.2f}".format(rate_threedose_lastwk - rate_threedose_twowk)
)

## The change in vaccination rate for one dose (whole population) between latest 2 weeks

onedose_ratechange_pop = float(
    "{:.2f}".format(rate_onedose_pop_lastwk - rate_onedose_pop_twowk)
)

## The change in vaccination rate for two doses (whole population) between latest 2 weeks

twodose_ratechange_pop = float(
    "{:.2f}".format(rate_leasttwodose_pop_lastwk - rate_leasttwodose_pop_twowk)
)

## The change in vaccination rate for three doses for the eligible population between latest 2 weeks

threedose_ratechange_pop = float(
    "{:.2f}".format(rate_threedose_pop_lastwk - rate_threedose_pop_twowk)
)

## Create a .json file so that we can insert values 'live' to html

# Data to be written
data_dictionary = {
    "eligible_one_dose": one_dose_swe,
    "eligible_two_doses": least_two_dose_swe,
    "eligible_three_doses": third_dose_swe,
    "eligible_four_doses": fourth_dose_swe,
    "eligible_one_dose_lastweek": rate_onedose_lastwk,
    "eligible_two_doses_lastweek": rate_leasttwodose_lastwk,
    "eligible_three_doses_lastweek": rate_threedose_lastwk,
    "eligible_one_dose_rate_change": onedose_ratechange,
    "eligible_two_doses_rate_change": twodose_ratechange,
    "eligible_three_doses_rate_change": threedose_ratechange,
    "population_one_dose": one_dose_pop,
    "population_two_doses": least_two_dose_pop,
    "population_three_doses": third_vacc_dose_pop,
    "population_four_doses": fourth_dose_pop,
    "population_one_dose_lastweek": rate_onedose_pop_lastwk,
    "population_two_doses_lastweek": rate_leasttwodose_pop_lastwk,
    "population_three_doses_lastweek": rate_threedose_pop_lastwk,
    "population_one_dose_rate_change": onedose_ratechange_pop,
    "population_two_doses_rate_change": twodose_ratechange_pop,
    "population_three_doses_rate_change": threedose_ratechange_pop,
}

with open("live_text_inserts.json", "w") as outfile:
    json.dump(data_dictionary, outfile)

# REMINDER FOR FOURTH DOSE ADDITION: ADD JSON FILE ADDITIONS TO PORTAL PAGE.
