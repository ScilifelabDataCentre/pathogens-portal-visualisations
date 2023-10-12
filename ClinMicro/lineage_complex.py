import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime as dt


# Import data
strain_data = pd.read_csv(
    "data/Uppsala_data_2023-10-08_complete.csv",
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
# lineage groups 1-4 could potentially be used - perhaps 1 and 2 groups are most useful

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

print(lineage1_perc)

# Work on lineage 2

group_lineage_two = (
    strain_data.groupby(["Year-Week", "lineage_groups02"])
    .size()
    .reset_index(name="no_lineage2")
)

lineage2_perc = pd.merge(
    group_lineage_two,
    number_samples_weekly,
    how="left",
    on="Year-Week",
)

lineage2_perc["percentage"] = (
    lineage2_perc["no_lineage2"] / lineage2_perc["strains_weekly"]
) * 100


def update_prop_graph(variants, lineage_groups):
    # ddf1 = Strain_percs[(Strain_percs["Strain"].isin(variant))]
    # dateline = date_val
    colours = px.colors.qualitative.Dark24
    fig = px.area(
        variants,
        x="date",
        y="percentage",
        color=lineage_groups,
        line_group=lineage_groups,
        color_discrete_map={
            lineage_groups[0]: colours[0],
            lineage_groups[1]: colours[1],
            lineage_groups[2]: colours[2],
            lineage_groups[3]: colours[3],
            lineage_groups[4]: colours[4],
            lineage_groups[5]: colours[5],
            lineage_groups[6]: colours[6],
            lineage_groups[7]: colours[7],
            lineage_groups[8]: colours[8],
            lineage_groups[9]: colours[9],
            lineage_groups[10]: colours[10],
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
        font={"size": 20},
        width=2000,
        height=1000,
        margin=dict(r=0, t=100, b=0, l=0),
        # showlegend=False,
        legend=dict(
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.01,
            font=dict(size=20),
            title="<b>Lineage</b><br>",
        ),
        hovermode="x unified",
        xaxis={
            "title": "<b><br>Date</b>",
            "tickangle": 0,
            "hoverformat": "%b %d, %Y (week %W)",
        },
    )
    fig.update_traces(hovertemplate="%{y:.2f}%"),
    # fig.add_vline(
    #     x=dateline, line_width=3, line_color="darkslategrey", line_dash="dash"
    # )
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
                                {"visible": [True]},
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
                pad={"r": 10, "t": 20},
                showactive=True,
                x=1.05,
                xanchor="left",
                y=1.1,
                yanchor="top",
            ),
            dict(
                buttons=list(
                    [
                        dict(
                            label="Whole timeline",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": (
                                        min(variants.date),
                                        max(variants.date),
                                    ),
                                    "yaxis.range": (
                                        min(variants.percentage),
                                        (max(variants.percentage)),
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
                                            max(variants.date)
                                            + pd.Timedelta(-16, unit="w")
                                        ),
                                        max(variants.date),
                                    ),
                                    "yaxis.range": (
                                        min(variants.percentage),
                                        (max(variants.percentage)),
                                    ),
                                },
                            ],
                        ),
                    ],
                ),
                type="buttons",
                # direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.1,
                yanchor="top",
            ),
        ]
    )
    fig.show()


update_prop_graph(lineage1_perc, "lineage_groups01")
