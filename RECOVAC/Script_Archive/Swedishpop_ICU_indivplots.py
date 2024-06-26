import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime as dt

# Import data

RECO_icu_18plus = pd.read_excel(
    "data/iva_vacc_18plus_23 Feb 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_icu_18to59 = pd.read_excel(
    "data/iva_vacc_18-59_23 Feb 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_icu_60plus = pd.read_excel(
    "data/iva_vacc_60plus_23 Feb 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# set date function


def date_func(dataset):
    dataset[["Year", "Week"]] = (
        dataset["wk"].str.split("w", expand=True).astype(int)
    )  # break apart week and year
    dataset["day"] = 1  # set day as Monday
    dataset.drop(dataset[(dataset["Year"] == 2019)].index, inplace=True)
    dataset["date"] = dataset.apply(
        lambda row: dt.fromisocalendar(row["Year"], row["Week"], row["day"]), axis=1
    )
    pd.to_datetime(dataset["date"])
    dataset.drop(columns=["Week", "Year", "day", "wk"], axis=1, inplace=True)
    dataset["date"] = dataset["date"].astype(str)
    # print(dataset.head())


datasets = {
    "icu_18plus": RECO_icu_18plus,
    "icu_18to59": RECO_icu_18to59,
    "icu_60plus": RECO_icu_60plus,
}

for name, df in datasets.items():
    date_func(df)

# datasets = [RECO_icu_18plus, RECO_icu_18to59, RECO_icu_60plus]

# # run the functions to recalculate the proportions and format the date
# for x in datasets:
#     date_func(x)

# # Make stacked bar chart

map_colour = px.colors.diverging.RdBu
map_colour[5] = "rgb(235, 235, 0)"


def ICU_bar_func(dataset, name):
    RECO = dataset
    fig = go.Figure(
        data=[
            go.Bar(
                name="Four Doses",
                x=RECO.date,
                y=RECO.vacc4,
                marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
                customdata=(RECO["c19_i1"]),
                hovertemplate="%{y} <b>Tot</b>: %{customdata}",
            ),
            go.Bar(
                name="Three Doses",
                x=RECO.date,
                y=RECO.vacc3,
                marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="Two Doses",
                x=RECO.date,
                y=RECO.vacc2,
                marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="One Dose",
                x=RECO.date,
                y=RECO.vacc1,
                marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
            ),
            go.Bar(
                name="No Doses",
                x=RECO.date,
                y=RECO.vacc0,
                marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
                # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
                # text=RECO_intense["c19_i1"],
                # textposition="outside",
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=False,
        font=dict(size=18),
        margin=dict(r=250, t=0, b=0, l=0),
        width=1500,
        height=800,
        # legend=dict(
        #     y=0.95, x=1.05, title="<b>Vaccination<br>Status</b>", font=dict(size=22)
        # ),
        showlegend=True,
        hoverlabel=dict(align="left"),
        hovermode="x unified",
    )

    # below - code
    # fig.add_vline(
    #     x=dt.strptime("2020-12-21", "%Y-%m-%d").timestamp() * 1000,
    #     annotation_position="top left",
    #     #    annotation=dict(font_size=16),
    #     annotation_text="First doses start ",
    #     line_width=2,
    # )

    # fig.add_vline(
    #     x=dt.strptime("2021-01-04", "%Y-%m-%d").timestamp() * 1000,
    #     annotation_text=" Second doses start",
    #     line_width=2,
    # )

    # fig.add_vline(
    #     x=dt.strptime("2020-12-21", "%Y-%m-%d").timestamp() * 1000,
    #     annotation_text="Third vaccinations",
    # )

    # modify x-axis
    fig.update_xaxes(
        title="<br><b>Date</b>",
        showgrid=True,
        linecolor="black",
        # range=["2020-01-01", max(RECO.date)],
    )

    highest_y_value = max(
        RECO["c19_i1"],
    )

    # modify y-axis
    fig.update_yaxes(
        title="<b>Admissions to ICU<br></b>",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=50,
        range=[0, int(highest_y_value * 1.1)],
    )
    if not os.path.isdir("Plots/"):
        os.mkdir("Plots/")
    # fig.show()
    fig.write_image(
        "Plots/ICUadmiss_vaccinationlevel_{}.png".format(name)
    )  # would need to change to json for portal


# single tests
# ICU_bar_func(RECO_iva_18plus, "18plus_icu")

# run all graphs
datasets = {
    "icu_18plus": RECO_icu_18plus,
    "icu_18to59": RECO_icu_18to59,
    "icu_60plus": RECO_icu_60plus,
}

for name, df in datasets.items():
    ICU_bar_func(df, name)
