import plotly.express as px
import pandas as pd
from datetime import datetime as dt

# Load the processed weekly data
lineage6_perc = pd.read_csv("https://blobserver.dc.scilifelab.se/blob/lineage-cleaned-data.csv")


# # Now need to format dates in a manner recognisable to plotly
lineage6_perc["year"] = (lineage6_perc["Year-Week"].str[:4]).astype(int)
lineage6_perc["week_no"] = lineage6_perc["Year-Week"].str[-3:]
lineage6_perc["week_no"] = (
    lineage6_perc["week_no"].str.replace("-", "", regex=True)
).astype(int)
# set the date to the start of the week (Monday)
lineage6_perc["day"] = 1
lineage6_perc["date"] = lineage6_perc.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)

lineage6_perc = lineage6_perc[(lineage6_perc["date"] > "2023-10-01")]

def condition(x):
    if x == "KP.3.1.1*":
        return 1
    elif x == "KP.* Other":
        return 2
    elif x == "Non KP JN.1*":
        return 3
    elif x == "JN.2*":
        return 4
    elif x == "BA.2.86* and JN* Other":
        return 5
    elif x == "XBB*":
        return 6
    elif x == "XEC":
        return 7
    elif x == "Omicron Other":
        return 8
    else:
        return 9


lineage6_perc["sort_lineages"] = lineage6_perc["lineage_groups06"].apply(condition)

# NB: an wrror may be thrown if the lineage is not in the dictionary.
lineage6_perc.sort_values(by=["sort_lineages"], inplace=True)

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
    lineage6_perc,
    x="date",
    y="percentage_lineage6",
    color="lineage_groups06",
    line_group="lineage_groups06",
    color_discrete_map={
        lineage6_perc.lineage_groups06.unique()[i]: colours[i]
        for i in range(len(lineage6_perc.lineage_groups06.unique()))
    },
    hover_data={
        "percentage_lineage6": ":.2f",
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
    margin=dict(r=0, t=180, b=120, l=0),
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
                        label="Data since Oct 2023",
                        method="relayout",
                        args=[
                            {
                                "xaxis.range": (
                                    min(lineage6_perc.date),
                                    max(lineage6_perc.date),
                                ),
                                "yaxis.range": (
                                    min(lineage6_perc.percentage_lineage6),
                                    (max(lineage6_perc.percentage_lineage6)),
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
                                        max(lineage6_perc.date)
                                        + pd.Timedelta(-16, unit="w")
                                    ),
                                    max(lineage6_perc.date),
                                ),
                                "yaxis.range": (
                                    min(lineage6_perc.percentage_lineage6),
                                    (max(lineage6_perc.percentage_lineage6)),
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
# fig.write_json("lineage_six_recent.json")
print(fig.to_json())