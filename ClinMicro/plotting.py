import plotly.express as px
import pandas as pd

# Load the processed weekly data
lineage5_perc = pd.read_csv("data/weekly_data1.csv")


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
    margin=dict(r=0, t=180, b=120, l=0),
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
                        label="Data since Oct 2023",
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
                                        pd.to_datetime(max(lineage5_perc.date))
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
fig.show()
# Prints as a json file
# fig.write_json("lineage_five_recent.json")
