import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime as dt


# Import data
strain_data = pd.read_csv(
    "data/Uppsala_data_2023-11-03.csv",
    sep=",",
)

# express date Year and week for grouping
strain_data["date"] = pd.to_datetime(strain_data["date"])
strain_data["Year-Week"] = strain_data["date"].dt.strftime("%Y-%W")
# Jan 1st 2023 is Sunday before the new week, so shows as 2023-00
strain_data["Year-Week"] = strain_data["Year-Week"].apply(
    lambda x: x.replace("2023-00", "2022-52")
)

# Need to calculate percentages strain as a percentage.
# Need total entries per week and each strain as a percentage of that.
# create dataset showing how many samples each week

number_samples_weekly = (
    strain_data.groupby(["Year-Week"]).size().reset_index(name="strains_weekly")
)

# Now calculate how many of each strain in each week (multiple means of classifying strains)
# lineage groups 1-4 could potentially be used - this plot works on whole timeline, and focuses on group 1

# Work on lineage 1

group_lineage_one = (
    strain_data.groupby(["Year-Week", "lineage_groups01"])
    .size()
    .reset_index(name="no_lineage1")
)

lineage1_perc = pd.merge(
    group_lineage_one,
    number_samples_weekly,
    how="left",
    on="Year-Week",
)

lineage1_perc["percentage"] = (
    lineage1_perc["no_lineage1"] / lineage1_perc["strains_weekly"]
) * 100

# # Now need to format dates in a manner recognisable to plotly
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
# print(lineage1_perc)


def update_prop_graph(variants, lineage_groups):
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
        variants,
        x="date",
        y="percentage",
        color="lineage_groups01",
        line_group="lineage_groups01",
        color_discrete_map={
            lineage1_perc.lineage_groups01.unique()[i]: colours[i]
            for i in range(len(lineage1_perc.lineage_groups01.unique()))
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
            # dict(
            #     buttons=list(
            #         [
            #             dict(
            #                 label="Whole timeline",
            #                 method="relayout",
            #                 args=[
            #                     {
            #                         "xaxis.range": (
            #                             min(variants.date),
            #                             max(variants.date),
            #                         ),
            #                         "yaxis.range": (
            #                             min(variants.percentage),
            #                             (max(variants.percentage)),
            #                         ),
            #                     },
            #                 ],
            #             ),
            #             dict(
            #                 label="Last 16 weeks",
            #                 method="relayout",
            #                 args=[
            #                     {
            #                         "xaxis.range": (
            #                             (
            #                                 max(variants.date)
            #                                 + pd.Timedelta(-16, unit="w")
            #                             ),
            #                             max(variants.date),
            #                         ),
            #                         "yaxis.range": (
            #                             min(variants.percentage),
            #                             (max(variants.percentage)),
            #                         ),
            #                     },
            #                 ],
            #             ),
            #         ],
            #     ),
            #     type="buttons",
            #     # direction="right",
            #     pad={"r": 0, "t": 15},
            #     showactive=True,
            #     x=0,
            #     xanchor="left",
            #     y=1.13,
            #     yanchor="top",
            # ),
        ]
    )
    # fig.show()
    # Prints as a json file
    fig.write_json("lineage_one_wholetime.json")


update_prop_graph(lineage1_perc, "lineage_groups01")
