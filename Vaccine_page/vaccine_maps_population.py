import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

from vaccine_dataprep_Swedentots import (
    df_vacc_lan,  # data on 1st 2 doses
    third_vacc_dose_lan,  # data on 3rd dose (note, this data comes from the age group tab 'totals')
    # The above could be changed for the timeseries data, but they're equilavent for now (Feb 2022), might change in future
    # these two were used historically because we didn't have time series for 3rd dose
    # and the åldersgrupp data for first doses didnt include all the age groups that were in the time series
    fourth_vacc_dose_lan,
    # Added fourth dose March 25th 2022
    SCB_population,  # raw population counts for each lan
)

# map
with open("sweden-counties.geojson", "r") as sw:
    jdata = json.load(sw)

# dictionary to match data and map
counties_id_map = {}
for feature in jdata["features"]:
    feature["id"] = feature["properties"]["cartodb_id"]
    counties_id_map[feature["properties"]["name"]] = feature["id"]

# There will be 3 maps, one for each dose
# Need to make calculation based on population data - need to match SCB population data

# First and second doses
df_vacc_lan = pd.merge(
    df_vacc_lan, SCB_population, how="left", left_on="Region", right_on="Lan"
)

df_vacc_lan["Vacc_perc_population"] = (
    df_vacc_lan["Antal vaccinerade"] / df_vacc_lan["Population"]
) * 100

# Third dose
third_vacc_dose_lan = pd.merge(
    third_vacc_dose_lan, SCB_population, how="left", left_on="Region", right_on="Lan"
)

third_vacc_dose_lan["Vacc_perc_population"] = (
    third_vacc_dose_lan["Antal vaccinerade"] / third_vacc_dose_lan["Population"]
) * 100

# Fourth dose
fourth_vacc_dose_lan = pd.merge(
    fourth_vacc_dose_lan, SCB_population, how="left", left_on="Region", right_on="Lan"
)

fourth_vacc_dose_lan["Vacc_perc_population"] = (
    fourth_vacc_dose_lan["Antal vaccinerade"] / fourth_vacc_dose_lan["Population"]
) * 100

# First and second doses are taken from a time series and are held together
# So, we need to seperate out the doses, and select only the latest data

# get data for one dose
one_dose_lan_pop = df_vacc_lan[
    (df_vacc_lan["date"] == df_vacc_lan["date"].max())
    & (df_vacc_lan["Vaccinationsstatus"] == "Minst 1 dos")
]

# drop the data for all Sweden in total, we don't need it
one_dose_lan_pop.drop(
    one_dose_lan_pop[(one_dose_lan_pop["Region"] == "Sweden")].index, inplace=True
)

# Change label for dose level to English
one_dose_lan_pop = one_dose_lan_pop.replace("Minst 1 dos", "One dose")

# Isolate data for 'at least two doses'
two_dose_lan_pop = df_vacc_lan[
    (df_vacc_lan["date"] == df_vacc_lan["date"].max())
    & (df_vacc_lan["Vaccinationsstatus"] == "Minst 2 doser")
]

# drop data for totals for Sweden
two_dose_lan_pop.drop(
    two_dose_lan_pop[(two_dose_lan_pop["Region"] == "Sweden")].index, inplace=True
)

# Change for second dose to English
two_dose_lan_pop = two_dose_lan_pop.replace("Minst 2 doser", "Two doses")

# third dose

# We don't want individual values for each age groups, just grab the 'totals' across the groups
third_vacc_dose_lan_pop = third_vacc_dose_lan[
    (third_vacc_dose_lan["Åldersgrupp"] == "Totalt")
]

# Drop th overall 'Sweden data', we don't need it
third_vacc_dose_lan_pop.drop(
    third_vacc_dose_lan_pop[(third_vacc_dose_lan_pop["Region"] == "Sweden")].index,
    inplace=True,
)

# Change label on dose level to English
third_vacc_dose_lan_pop = third_vacc_dose_lan_pop.replace("3 doser", "Three doses")

# fourth dose

# We don't want individual values for each age groups, just grab the 'totals' across the groups
fourth_vacc_dose_lan_pop = fourth_vacc_dose_lan[
    (fourth_vacc_dose_lan["Åldersgrupp"] == "Totalt")
]

# Drop th overall 'Sweden data', we don't need it
fourth_vacc_dose_lan_pop.drop(
    fourth_vacc_dose_lan_pop[(fourth_vacc_dose_lan_pop["Region"] == "Sweden")].index,
    inplace=True,
)

# Change label on dose level to English
fourth_vacc_dose_lan_pop = fourth_vacc_dose_lan_pop.replace("4 doser", "Four doses")
# print(fourth_vacc_dose_lan_pop["Procent vaccinerade"])
# Tie each dataframe to the map
# one dose
one_dose_lan_pop["id"] = one_dose_lan_pop["Region"].apply(lambda x: counties_id_map[x])
# two doses
two_dose_lan_pop["id"] = two_dose_lan_pop["Region"].apply(lambda x: counties_id_map[x])
# three doses
third_vacc_dose_lan_pop["id"] = third_vacc_dose_lan_pop["Region"].apply(
    lambda x: counties_id_map[x]
)
# four doses
fourth_vacc_dose_lan_pop["id"] = fourth_vacc_dose_lan_pop["Region"].apply(
    lambda x: counties_id_map[x]
)

# Now create maps
# Some variables common to all maps

map_colour = px.colors.diverging.RdBu
map_colour[5] = "rgb(255,255,204)"
splits = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0]
lat_foc = 62.45
lon_foc = 20.5

# Map function (single maps - first 3 doses)


def map_func(dataset, dose):
    fig = px.choropleth(
        dataset,
        geojson=jdata,
        locations="id",
        color=dataset["Vacc_perc_population"],
        # Below gives discrete colours for ranges
        color_continuous_scale=[
            (splits[0], map_colour[10]),
            (splits[1], map_colour[10]),
            (splits[1], map_colour[9]),
            (splits[2], map_colour[9]),
            (splits[2], map_colour[8]),
            (splits[3], map_colour[8]),
            (splits[3], map_colour[7]),
            (splits[4], map_colour[7]),
            (splits[4], map_colour[6]),
            (splits[5], map_colour[6]),
            (splits[5], map_colour[5]),
            (splits[6], map_colour[5]),
            (splits[6], map_colour[4]),
            (splits[7], map_colour[4]),
            (splits[7], map_colour[3]),
            (splits[8], map_colour[3]),
            (splits[8], map_colour[2]),
            (splits[9], map_colour[2]),
            (splits[9], map_colour[1]),
            (splits[10], map_colour[1]),
        ],
        # this keeps the range of colours constant regardless of data
        range_color=[0, 100],
        scope="europe",
        hover_name="Region",
        hover_data={
            "Vacc_perc_population": ":.2f",
            "Vaccinationsstatus": True,
            "id": False,
        },
        labels={
            "Vacc_perc_population": "Percentage of population<br>vaccinated (%)",
            "Vaccinationsstatus": "<br>Number of Doses",
        },
    )
    # this section deals with the exact focus on the map
    fig.update_layout(
        geo=dict(
            lonaxis_range=[20, 90],  # the logitudinal range to consider
            lataxis_range=[48, 100],  # the logitudinal range to consider
            projection_scale=4.55,  # this is kind of like zoom
            center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
            visible=False,
        )
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(dragmode=False)
    # The below labels the colourbar categories
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="<b>Percentage of population<br>vaccinated with<br>" + dose + "</b>",
            tickvals=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
            ticktext=[
                "00.00 - 9.99%",
                "10.00 - 19.99%",
                "20.00 - 29.99%",
                "30.00 - 39.99%",
                "40.00 - 49.99%",
                "50.00 - 59.99%",
                "60.00 - 69.99%",
                "70.00 - 79.99%",
                "80.00 - 89.99%",
                "90.00 - 100.00%",
            ],
            x=0.51,
            y=0.40,
            thicknessmode="pixels",
            thickness=10,
            lenmode="pixels",
            len=285,
        ),
        font=dict(size=12),
    )
    fig.update_traces(marker_line_color="white")

    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    fig.write_json("Plots/{}_pop_map.json".format(name))


datasets = {
    "one dose": one_dose_lan_pop,
    "two doses": two_dose_lan_pop,
    "three doses": third_vacc_dose_lan_pop,
    "four doses": fourth_vacc_dose_lan_pop,
}

for name, df in datasets.items():
    map_func(df, name)

# Need a map showing data on eligibility method for 4th dose too. Create this independently


def eligible_map_func(elig_data, dose):
    fig = px.choropleth(
        elig_data,
        geojson=jdata,
        locations="id",
        color=elig_data["Procent vaccinerade"],
        # Below gives discrete colours for ranges
        color_continuous_scale=[
            (splits[0], map_colour[10]),
            (splits[1], map_colour[10]),
            (splits[1], map_colour[9]),
            (splits[2], map_colour[9]),
            (splits[2], map_colour[8]),
            (splits[3], map_colour[8]),
            (splits[3], map_colour[7]),
            (splits[4], map_colour[7]),
            (splits[4], map_colour[6]),
            (splits[5], map_colour[6]),
            (splits[5], map_colour[5]),
            (splits[6], map_colour[5]),
            (splits[6], map_colour[4]),
            (splits[7], map_colour[4]),
            (splits[7], map_colour[3]),
            (splits[8], map_colour[3]),
            (splits[8], map_colour[2]),
            (splits[9], map_colour[2]),
            (splits[9], map_colour[1]),
            (splits[10], map_colour[1]),
        ],
        # this keeps the range of colours constant regardless of data
        range_color=[0, 100],
        scope="europe",
        hover_name="Region",
        hover_data={
            "Procent vaccinerade": ":.2f",
            "Vaccinationsstatus": True,
            "id": False,
        },
        labels={
            "Procent vaccinerade": "Percentage of eligible<br>population vaccinated (%)",
            "Vaccinationsstatus": "<br>Number of Doses",
        },
    )
    # this section deals with the exact focus on the map
    fig.update_layout(
        geo=dict(
            lonaxis_range=[20, 90],  # the logitudinal range to consider
            lataxis_range=[48, 100],  # the logitudinal range to consider
            projection_scale=4.55,  # this is kind of like zoom
            center=dict(lat=lat_foc, lon=lon_foc),  # this will center on the point
            visible=False,
        )
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(dragmode=False)
    # The below labels the colourbar categories
    fig.update_layout(
        coloraxis_colorbar=dict(
            title="<b>Percentage of eligible<br>population vaccinated with<br>"
            + dose
            + "</b>",
            tickvals=[5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
            ticktext=[
                "00.00 - 9.99%",
                "10.00 - 19.99%",
                "20.00 - 29.99%",
                "30.00 - 39.99%",
                "40.00 - 49.99%",
                "50.00 - 59.99%",
                "60.00 - 69.99%",
                "70.00 - 79.99%",
                "80.00 - 89.99%",
                "90.00 - 100.00%",
            ],
            x=0.51,
            y=0.40,
            thicknessmode="pixels",
            thickness=10,
            lenmode="pixels",
            len=285,
        ),
        font=dict(size=12),
    )
    fig.update_traces(marker_line_color="white")
    # fig.show()
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    fig.write_json("Plots/{}_elig_map.json".format(name))
    # fig.write_image("Plots/{}_elig_map.png".format(name))


elig_datasets = {
    "four doses": fourth_vacc_dose_lan_pop,
}

for name, df in elig_datasets.items():
    eligible_map_func(df, name)
