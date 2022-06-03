import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime as dt

# Import data

RECO_icu_18plus = pd.read_excel(
    "data/iva_vacc_18plus_25 May 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_icu_18to59 = pd.read_excel(
    "data/iva_vacc_18-59_25 May 2022.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

RECO_icu_60plus = pd.read_excel(
    "data/iva_vacc_60plus_25 May 2022.xlsx",
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

# # Make stacked bar chart

map_colour = px.colors.diverging.RdBu
map_colour[5] = "rgb(235, 235, 0)"
# print(map_colour[10])

# def ICU_bar_func(dataset, name):
#     RECO = dataset
fig = go.Figure(
    data=[
        # data on 18+
        go.Bar(
            name="Four Doses",
            x=RECO_icu_18plus.date,
            y=RECO_icu_18plus.vacc4,
            marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
            customdata=(RECO_icu_18plus["c19_i1"]),
            hovertemplate="%{y} <b>Tot</b>: %{customdata}",
        ),
        go.Bar(
            name="Three Doses",
            x=RECO_icu_18plus.date,
            y=RECO_icu_18plus.vacc3,
            marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Two Doses",
            x=RECO_icu_18plus.date,
            y=RECO_icu_18plus.vacc2,
            marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="One Dose",
            x=RECO_icu_18plus.date,
            y=RECO_icu_18plus.vacc1,
            marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="No doses",
            x=RECO_icu_18plus.date,
            y=RECO_icu_18plus.vacc0,
            marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
            # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
            # text=RECO_intense["c19_i1"],
            # textposition="outside",
        ),
        # data 18-59
        go.Bar(
            name="Four Doses",
            x=RECO_icu_18to59.date,
            y=RECO_icu_18to59.vacc4,
            visible=False,
            marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
            customdata=(RECO_icu_18to59["c19_i1"]),
            hovertemplate="%{y} <b>Tot</b>: %{customdata}",
        ),
        go.Bar(
            name="Three Doses",
            x=RECO_icu_18to59.date,
            y=RECO_icu_18to59.vacc3,
            visible=False,
            marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Two Doses",
            x=RECO_icu_18to59.date,
            y=RECO_icu_18to59.vacc2,
            visible=False,
            marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="One Dose",
            x=RECO_icu_18to59.date,
            y=RECO_icu_18to59.vacc1,
            visible=False,
            marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
        ),
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
        # data 60+
        go.Bar(
            name="Four Doses",
            x=RECO_icu_60plus.date,
            y=RECO_icu_60plus.vacc4,
            visible=False,
            marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
            customdata=(RECO_icu_60plus["c19_i1"]),
            hovertemplate="%{y} <b>Tot</b>: %{customdata}",
        ),
        go.Bar(
            name="Three Doses",
            x=RECO_icu_60plus.date,
            y=RECO_icu_60plus.vacc3,
            visible=False,
            marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Two Doses",
            x=RECO_icu_60plus.date,
            y=RECO_icu_60plus.vacc2,
            visible=False,
            marker=dict(color=map_colour[5], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="One Dose",
            x=RECO_icu_60plus.date,
            y=RECO_icu_60plus.vacc1,
            visible=False,
            marker=dict(color=map_colour[3], line=dict(color="#000000", width=1)),
        ),
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
    ]
)

fig.update_layout(
    barmode="stack",
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=12),
    margin=dict(r=100, t=175, b=0, l=0),
    # width=1500,
    # height=800,
    legend=dict(title="<b>Vaccine Doses</b>"),
    showlegend=True,
    hoverlabel=dict(align="left"),
    hovermode="x unified",
)

# modify x-axis
fig.update_xaxes(
    title="<br><b>Date</b>",
    showgrid=True,
    linecolor="black",
    # range=["2020-01-01", max(RECO.date)],
)

highest_y_value = max(
    RECO_icu_18plus["c19_i1"],
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

button_layer_1_height = 1.57
button_layer_2_height = 1.35
button_layer_3_height = 1.22

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
                            # {"title": "", "annotations": []},
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
                                ]
                            },
                            # {"title": "", "annotations": []},
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
                                    True,
                                    True,
                                    True,
                                    True,
                                    True,
                                ]
                            },
                            # {"title": "", "annotations": []},
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
                        label="Whole time series",
                        method="relayout",
                        args=[
                            "xaxis.range",
                            (min(RECO_icu_18plus.date), max(RECO_icu_18plus.date)),
                        ],
                    ),
                    dict(
                        label="Align timeline",
                        method="relayout",
                        args=[
                            "xaxis.range",
                            ("2020-12-21", max(RECO_icu_18plus.date)),
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
            x=-0.1,
            xref="paper",
            y=1.50,
            yref="paper",
            align="left",
            showarrow=False,
        ),
        dict(
            text="Timeframe:",
            x=-0.1,
            xref="paper",
            y=1.30,
            yref="paper",
            showarrow=False,
        ),
    ]
)

if not os.path.isdir("Plots/"):
    os.mkdir("Plots/")
# fig.show()
fig.write_json("Plots/ICUadmiss_vaccinationlevel_button.json")
