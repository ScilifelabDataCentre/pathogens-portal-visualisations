import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime as dt


# Import data
strain_data = pd.read_csv(
    "data/Uppsala_data_2023-10-30.csv",
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

group_lineage_four = (
    strain_data.groupby(["Year-Week", "lineage_groups04"])
    .size()
    .reset_index(name="no_lineage4")
)

lineage4_perc = pd.merge(
    group_lineage_four,
    number_samples_weekly,
    how="left",
    on="Year-Week",
)

lineage4_perc["percentage"] = (
    lineage4_perc["no_lineage4"] / lineage4_perc["strains_weekly"]
) * 100

# # Now need to format dates in a manner recognisable to plotly
lineage4_perc["year"] = (lineage4_perc["Year-Week"].str[:4]).astype(int)
lineage4_perc["week_no"] = lineage4_perc["Year-Week"].str[-3:]
lineage4_perc["week_no"] = (
    lineage4_perc["week_no"].str.replace("-", "", regex=True)
).astype(int)
# set the date to the start of the week (Monday)
lineage4_perc["day"] = 1
lineage4_perc["date"] = lineage4_perc.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)

# print(lineage4_perc)


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
    "#D30000",
    "#151B54",
    "#FFF200",
    "#B200ED",
    "#8D021F",
    "#0000FF",
]
fig = px.area(
    lineage4_perc,
    x="date",
    y="percentage",
    color="lineage_groups04",
    line_group="lineage_groups04",
    color_discrete_map={
        lineage4_perc.lineage_groups04.unique()[i]: colours[i]
        for i in range(len(lineage4_perc.lineage_groups04.unique()))
    },
    hover_data={
        "percentage": ":.2f",
    },
)
fig.update_layout(
    title=" ",
    yaxis={
        "title": "<b>Percentage of Strains<br></b>",
        "ticktext": [" ", "20%", "40%", "60%", "80%", "100%"],
        "tickvals": ["0", "20", "40", "60", "80", "100"],
        "range": [0, 100],
    },
    font={"size": 12},
    autosize=True,
    margin=dict(r=0, t=100, b=120, l=0),
    # showlegend=False,
    legend=dict(
        yanchor="top",
        y=1.0,
        xanchor="left",
        x=1.01,
        font=dict(size=12),
        title="<b>Lineage</b><br>",
    ),
    hovermode="x unified",
    xaxis={
        "title": "<b>Date</b>",
        "tickangle": 0,
        "hoverformat": "%b %d, %Y (week %W)",
        # Use this to show just the first 16 weeks in the first instance
        # "range": [
        #     (max(lineage4_perc.date) + pd.Timedelta(-16, unit="w")),
        #     (max(lineage4_perc["date"])),
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
                                    min(lineage4_perc.date),
                                    max(lineage4_perc.date),
                                ),
                                "yaxis.range": (
                                    min(lineage4_perc.percentage),
                                    (max(lineage4_perc.percentage)),
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
                                        max(lineage4_perc.date)
                                        + pd.Timedelta(-16, unit="w")
                                    ),
                                    max(lineage4_perc.date),
                                ),
                                "yaxis.range": (
                                    min(lineage4_perc.percentage),
                                    (max(lineage4_perc.percentage)),
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
