# Will create indicators to display on page
import argparse
import pandas as pd
import os
import json

# Import processed data
from vaccine_dataprep_Swedentots import (
    first_two_timeseries,
    third_timseries,
    fourth_timseries,
    Swedish_population,
)

def float_str(flt):
    return float("{:.2f}".format(flt))

def parse_dose_data(dose_data, dose_filter=None):
    dose_data["Vacc_perc_population"] = (dose_data["Antal vaccinerade"]/Swedish_population) * 100
    if dose_filter:
        dose_data = dose_data[dose_data["Vaccinationsstatus"] == dose_filter]
    last_three_weeks_data = []
    pop_last_three_weeks_data = []
    for ind in range(1,4):
        week_data = dose_data[dose_data["date"] == dose_data["date"].unique()[-abs(ind)]]
        last_three_weeks_data.append(float(week_data["Procent vaccinerade"].round(2)))
        pop_last_three_weeks_data.append(float(week_data["Vacc_perc_population"].round(2)))
    return (
        last_three_weeks_data[0],
        float_str(last_three_weeks_data[0] - last_three_weeks_data[1]),
        float_str((last_three_weeks_data[0] - last_three_weeks_data[1]) - \
                  (last_three_weeks_data[1] - last_three_weeks_data[2])),
        pop_last_three_weeks_data[0],
        float_str(pop_last_three_weeks_data[0] - pop_last_three_weeks_data[1]),
        float_str((pop_last_three_weeks_data[0] - pop_last_three_weeks_data[1]) - \
                  (pop_last_three_weeks_data[1] - pop_last_three_weeks_data[2]))
        )

aparser = argparse.ArgumentParser(description="Generate text insert json")
aparser.add_argument("--output-dir", nargs="?", default="vaccine_plots",
                     help="Output directory where the files will be saved")
args = aparser.parse_args()

one_dose_swe, rate_onedose_lastwk, onedose_ratechange,\
one_dose_pop, rate_onedose_pop_lastwk, onedose_ratechange_pop = parse_dose_data(first_two_timeseries, "Minst 1 dos")

least_two_dose_swe, rate_leasttwodose_lastwk, twodose_ratechange,\
least_two_dose_pop, rate_leasttwodose_pop_lastwk, twodose_ratechange_pop = parse_dose_data(first_two_timeseries, "Minst 2 doser")

third_dose_swe, rate_threedose_lastwk, threedose_ratechange,\
third_vacc_dose_pop, rate_threedose_pop_lastwk, threedose_ratechange_pop = parse_dose_data(third_timseries)

fourth_dose_swe, rate_fourdose_lastwk, fourdose_ratechange,\
fourth_vacc_dose_pop, rate_fourdose_pop_lastwk, fourdose_ratechange_pop = parse_dose_data(fourth_timseries)

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
    "eligible_four_doses_lastweek": rate_fourdose_lastwk,
    "eligible_one_dose_rate_change": onedose_ratechange,
    "eligible_two_doses_rate_change": twodose_ratechange,
    "eligible_three_doses_rate_change": threedose_ratechange,
    "eligible_four_doses_rate_change": fourdose_ratechange,
    "population_one_dose": one_dose_pop,
    "population_two_doses": least_two_dose_pop,
    "population_three_doses": third_vacc_dose_pop,
    "population_four_doses": fourth_vacc_dose_pop,
    "population_one_dose_lastweek": rate_onedose_pop_lastwk,
    "population_two_doses_lastweek": rate_leasttwodose_pop_lastwk,
    "population_three_doses_lastweek": rate_threedose_pop_lastwk,
    "population_four_doses_lastweek": rate_fourdose_pop_lastwk,
    "population_one_dose_rate_change": onedose_ratechange_pop,
    "population_two_doses_rate_change": twodose_ratechange_pop,
    "population_three_doses_rate_change": threedose_ratechange_pop,
    "population_four_doses_rate_change": fourdose_ratechange_pop,
}

if __name__ == "__main__":
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    with open(os.path.join(args.output_dir, "vaccine_text_inserts.json"), "w") as outfile:
        json.dump(data_dictionary, outfile)
