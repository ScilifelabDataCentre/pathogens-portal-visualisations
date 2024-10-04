import plotly.express as px
import pandas as pd
from datetime import datetime as dt
import pandas as pd
from datetime import datetime as dt


# Load the processed weekly data
lineage1_perc = pd.read_csv("https://blobserver.dc.scilifelab.se/blob/lineage-cleaned-data.csv")

# Now need to format dates in a manner recognisable to plotly
lineage1_perc["year"] = (lineage1_perc["Year-Week"].str[:4]).astype(int)
lineage1_perc["week_no"] = lineage1_perc["Year-Week"].str[-3:]
lineage1_perc["week_no"] = (
    lineage1_perc["week_no"].str.replace("-", "", regex=True)
).astype(int)

# set the date to the start of the week (Monday)
lineage1_perc["day"] = 1
lineage1_perc["date"] = lineage1_perc.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)

# sort values to ensure that the traces show in the desired order.
lineage1_perc.sort_values(by=["lineage_groups01"], ascending=False, inplace=True)

colours = [
    "#D30000",
    "#151B54",
    "#FFF200",
    "#B200ED",
    "#8D021F",
    "#0000FF",
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
]

fig = px.area(
    lineage1_perc,
    x="date",
    y="percentage_lineage1",
    color="lineage_groups01",
    line_group="lineage_groups01",
    color_discrete_map={
        lineage1_perc.lineage_groups01.unique()[i]: colours[i]
        for i in range(len(lineage1_perc.lineage_groups01.unique()))
    },
    hover_data={
        "percentage_lineage1": ":.2f",
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
        traceorder="reversed",
    ),
    hovermode="x unified",
    xaxis={
        "title": "<b>Date</b>",
        "tickangle": 0,
        "hoverformat": "%b %d, %Y (week %W)",
    },
)

fig.update_traces(hovertemplate="%{y:.2f}%")

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
    ]
)

# fig.show()

# Prints as a json file
# fig.write_json("lineage_one_wholetime.json")
print(fig.to_json())

