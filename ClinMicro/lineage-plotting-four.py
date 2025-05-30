import plotly.express as px
import pandas as pd
from datetime import datetime as dt

# Load the processed weekly data
lineage4_perc = pd.read_csv("https://blobserver.dc.scilifelab.se/blob/lineage-cleaned-data.csv")

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
lineage4_perc = lineage4_perc[(lineage4_perc["date"] > "2023-01-01")]

def condition(x):
    if x == "BA.1":
        return 1
    elif x == "BA.2":
        return 2
    elif x == "CH":
        return 3
    elif x == "DV.7.1":
        return 4
    elif x == "BA.2.75 Other":
        return 5
    elif x == "BA.2.86/Pirola":
        return 6
    elif x == "BA.4":
        return 7
    elif x == "BA.5":
        return 8
    elif x == "BQ":
        return 9
    elif x == "XBB.1.5":
        return 10
    elif x == "XBB.1.9.1":
        return 11
    elif x == "XBB.1.9.2":
        return 12
    elif x == "EG.5/Eris":
        return 13
    elif x == "XBB.1.16":
        return 14
    elif x == "XBB.2.3":
        return 15
    elif x == "XBB Other":
        return 16
    elif x == "Omicron Other":
        return 17
    else:
        return 18


lineage4_perc["sort_lineages"] = lineage4_perc["lineage_groups04"].apply(condition)

# NB: an wrror may be thrown if the lineage is not in the dictionary.
lineage4_perc.sort_values(by=["sort_lineages"], inplace=True)
# print(lineage4_perc)

# lineage4_perc.to_csv("data/four.csv", index=False)


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
    y="percentage_lineage4",
    color="lineage_groups04",
    line_group="lineage_groups04",
    color_discrete_map={
        lineage4_perc.lineage_groups04.unique()[i]: colours[i]
        for i in range(len(lineage4_perc.lineage_groups04.unique()))
    },
    hover_data={
        "percentage_lineage4": ":.2f",
    },
)
fig.update_layout(
    title=" ",
    yaxis={
        "title": "<b>Percentage of Lineages<br></b>",
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
        traceorder="normal",
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
                                    min(lineage4_perc.percentage_lineage4),
                                    (max(lineage4_perc.percentage_lineage4)),
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
                                    min(lineage4_perc.percentage_lineage4),
                                    (max(lineage4_perc.percentage_lineage4)),
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
# fig.write_json("lineage_four_recent.json")
print(fig.to_json())

