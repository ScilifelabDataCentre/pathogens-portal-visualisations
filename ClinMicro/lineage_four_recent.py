import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime as dt


# Import data
strain_data = pd.read_csv(
    "data/Uppsala_data_2024-02-06_Nextclade.csv",
    sep=",",
)

# express date Year and week for grouping
strain_data["date"] = pd.to_datetime(strain_data["date"])
strain_data["Year-Week"] = strain_data["date"].dt.strftime("%Y-%W")
# Jan 1st 2023 is Sunday before the new week, so shows as 2023-00
strain_data["Year-Week"] = strain_data["Year-Week"].apply(
    lambda x: x.replace("2023-00", "2022-52")
)

strain_data = strain_data[(strain_data["date"] > "2023-01-01")]

# print(strain_data)

# Need to calculate percentages strain as a percentage.
# Need total entries per week and each strain as a percentage of that.
# create dataset showing how many samples each week

number_samples_weekly = (
    strain_data.groupby(["Year-Week"]).size().reset_index(name="strains_weekly")
)

# Now calculate how many of each strain in each week (multiple means of classifying strains)
# lineage groups 1-4 could potentially be used - For this plot, use lineage group 4

# Work on lineage 1

group_lineage_five = (
    strain_data.groupby(["Year-Week", "lineage_groups05"])
    .size()
    .reset_index(name="no_lineage5")
)

lineage5_perc = pd.merge(
    group_lineage_five,
    number_samples_weekly,
    how="left",
    on="Year-Week",
)

lineage5_perc["percentage"] = (
    lineage5_perc["no_lineage5"] / lineage5_perc["strains_weekly"]
) * 100

# # Now need to format dates in a manner recognisable to plotly
lineage5_perc["year"] = (lineage5_perc["Year-Week"].str[:4]).astype(int)
lineage5_perc["week_no"] = lineage5_perc["Year-Week"].str[-3:]
lineage5_perc["week_no"] = (
    lineage5_perc["week_no"].str.replace("-", "", regex=True)
).astype(int)
# set the date to the start of the week (Monday)
lineage5_perc["day"] = 1
lineage5_perc["date"] = lineage5_perc.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)


def condition(x):
    if x == "BA.2":
        return 1
    elif x == "DV.7.1*":
        return 2
    elif x == "CH.*":
        return 3
    elif x == "BA.2.75* Other":
        return 4
    elif x == "JN.1*":
        return 5
    elif x == "JN.2*":
        return 6
    elif x == "JN.3*":
        return 7
    elif x == "BA.2.86* Other":
        return 8
    elif x == "BQ.*":
        return 9
    elif x == "JD.*":
        return 10
    elif x == "XBB.1.5* Other":
        return 11
    elif x == "FL.*":
        return 12
    elif x == "HK.*":
        return 13
    elif x == "JG.*":
        return 14
    elif x == "HV.*":
        return 15
    elif x == "EG.5.1* Other":
        return 16
    elif x == "EG.5* Other":
        return 17
    elif x == "XBB.1.9.2* Other":
        return 18
    elif x == "FU.*":
        return 19
    elif x == "XBB.1.16* Other":
        return 20
    elif x == "FY.*":
        return 21
    elif x == "XBB.2.3*":
        return 22
    elif x == "XBB* Other":
        return 23
    elif x == "XDA":
        return 24
    elif x == "XDD":
        return 25
    else:
        return 26


lineage5_perc["sort_lineages"] = lineage5_perc["lineage_groups05"].apply(condition)

# NB: an wrror may be thrown if the lineage is not in the dictionary.
lineage5_perc.sort_values(by=["sort_lineages"], inplace=True)
# print(lineage5_perc)

colours = [
    "#FCD12A",
    "#784B84",
    "#FF2400",
    "#1E90FF",
    "#D5B85A",
    "#81007F",
    "#CD5C5C",
    "#79BAEC",
    "#CC7722",
    "#DE73FF",
    "#421310",
    "#87AFC7",
    "#EFFD5F",
    "#7852A9",
    "#BF0A30",
    "#FFF200",
    "#151B54",
    "#D30000",
    "#B200ED",
    "#8D021F",
    "#0000FF",
    "#bf02af",
    "#0221bf",
    "#f7f302",
    "#030303",
    "#5c5c5b",
    "#5b5c5c",
    "#5602f2",
]
fig = px.area(
    lineage5_perc,
    x="date",
    y="percentage",
    color="lineage_groups05",
    line_group="lineage_groups05",
    color_discrete_map={
        lineage5_perc.lineage_groups05.unique()[i]: colours[i]
        for i in range(len(lineage5_perc.lineage_groups05.unique()))
    },
    hover_data={
        "percentage": ":.2f",
    },
)
fig.update_layout(
    title=" ",
    yaxis={
        "title": "<b>Percentage of Lineages<br></b>",
        "ticktext": [" ", "20%", "40%", "60%", "80%", "100%"],
        "tickvals": ["0", "20", "40", "60", "80", "100"],
        "range": [0, 100.1],
    },
    font={"size": 12},
    autosize=True,
    margin=dict(r=0, t=180, b=85, l=0),
    # showlegend=False,
    legend=dict(
        yanchor="top",
        y=1.0,
        xanchor="left",
        x=1.01,
        font=dict(size=12),
        title="<b>Lineage</b><br>",
        traceorder="normal",
    ),
    hovermode="x unified",
    xaxis={
        "title": "<b>Date</b>",
        "tickangle": 0,
        "hoverformat": "%b %d, %Y (week %W)",
        # Use this to show just the first 16 weeks in the first instance
        # "range": [
        #     (max(lineage5_perc.date) + pd.Timedelta(-16, unit="w")),
        #     (max(lineage5_perc["date"])),
        # ],
    },
)
fig.update_traces(hovertemplate="%{y:.2f}%"),
for i in range(len(fig["data"])):
    fig["data"][i]["line"]["width"] = 0

# Buttons

fig.update_layout(
    updatemenus=[
        dict(
            buttons=list(
                [
                    dict(
                        label="Select all lineages",
                        method="update",
                        args=[
                            {
                                "visible": [
                                    True,
                                ]
                            },
                        ],
                    ),
                    dict(
                        label="Deselect all lineages",
                        method="update",
                        args=[
                            {"visible": "legendonly"},
                        ],
                    ),
                ]
            ),
            type="buttons",
            # direction="right",
            pad={"r": 0, "t": 15},
            showactive=True,
            x=0.98,
            xanchor="left",
            y=1.23,
            yanchor="top",
        ),
        dict(
            buttons=list(
                [
                    dict(
                        label="Data since Jan 2023",
                        method="relayout",
                        args=[
                            {
                                "xaxis.range": (
                                    min(lineage5_perc.date),
                                    max(lineage5_perc.date),
                                ),
                                "yaxis.range": (
                                    min(lineage5_perc.percentage),
                                    (max(lineage5_perc.percentage)),
                                ),
                            },
                        ],
                    ),
                    dict(
                        label="Last 16 weeks",
                        method="relayout",
                        args=[
                            {
                                "xaxis.range": (
                                    (
                                        max(lineage5_perc.date)
                                        + pd.Timedelta(-16, unit="w")
                                    ),
                                    max(lineage5_perc.date),
                                ),
                                "yaxis.range": (
                                    min(lineage5_perc.percentage),
                                    (max(lineage5_perc.percentage)),
                                ),
                            },
                        ],
                    ),
                ],
            ),
            type="buttons",
            # direction="right",
            pad={"r": 0, "t": 15},
            showactive=True,
            x=0,
            xanchor="left",
            y=1.23,
            yanchor="top",
        ),
    ]
)
# fig.show()
# Prints as a json file
fig.write_json("lineage_four_recent.json")
