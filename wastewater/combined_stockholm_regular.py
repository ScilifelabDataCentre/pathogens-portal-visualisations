import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt

from plotly.io import write_image


wastewater_data = pd.read_csv(
    "https://datagraphics.dckube.scilifelab.se/api/dataset/65f19e61386a4a039aa798010ca42469.csv",
    sep=",",
)
wastewater_data["year"] = (wastewater_data["week"].str[:4]).astype(int)
wastewater_data["week_no"] = wastewater_data["week"].str[-3:]
wastewater_data["week_no"] = wastewater_data["week_no"].str.replace("*", "", regex=True)
wastewater_data["week_no"] = (
    wastewater_data["week_no"].str.replace("-", "", regex=True)
).astype(int)
# set the date to the start of the week (Monday)
wastewater_data["day"] = 1
wastewater_data["date"] = wastewater_data.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)
# want to initially limit the date range,
max_date = max(wastewater_data["date"])
min_date = max_date + pd.Timedelta(-16, unit="w")
# The below just helps to set the y axis, so that it varies according to values in the last 16 weeks
wastewater_data_res = wastewater_data[
    (wastewater_data["date"] >= min_date) & (wastewater_data["date"] <= max_date)
]

# colours for plot
colours = px.colors.diverging.RdBu

# Below sets a dataset for each city. Need to add to it if more places are added
# Will also need to add in a go.Scatter trace in the fig (no change needed to layout)
bromma_wwtp_jarva = wastewater_data[
    (wastewater_data["wwtp"] == "Bromma WWTP, Järva Inlet")
]
bromma_wwtp_riksby = wastewater_data[
    (wastewater_data["wwtp"] == "Bromma WWTP, Riksby Inlet")
]
bromma_wwtp_hasselby = wastewater_data[
    (wastewater_data["wwtp"] == "Bromma WWTP, Hässelby Inlet")
]
henriksdal_wwtp_henriksdal = wastewater_data[
    (wastewater_data["wwtp"] == "Henriksdal WWTP, Henriksdal Inlet")
]
henriksdal_wwtp_sickla = wastewater_data[
    (wastewater_data["wwtp"] == "Henriksdal WWTP, Sickla Inlet")
]
kappala_wwtp = wastewater_data[(wastewater_data["wwtp"] == "Käppala WWTP")]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        name="Bromma, Järva Inlet",
        x=bromma_wwtp_jarva.date,
        y=bromma_wwtp_jarva.value,
        mode="lines+markers",
        marker=dict(color=colours[0], size=7),
        marker_symbol="square",
        line=dict(color=colours[0], width=2),
    )
)

fig.add_trace(
    go.Scatter(
        name="Bromma, Riksby Inlet",
        x=bromma_wwtp_riksby.date,
        y=bromma_wwtp_riksby.value,
        mode="lines+markers",
        marker=dict(color=colours[1], size=7),
        marker_symbol="circle",
        line=dict(color=colours[1], width=2),
    )
)

fig.add_trace(
    go.Scatter(
        name="Bromma, Hässelby Inlet",
        x=bromma_wwtp_hasselby.date,
        y=bromma_wwtp_hasselby.value,
        mode="lines+markers",
        marker=dict(color=colours[3], size=7),
        marker_symbol="x",
        line=dict(color=colours[3], width=2),
    )
)

fig.add_trace(
    go.Scatter(
        name="Henriksdal, Henriksdal Inlet",
        x=henriksdal_wwtp_henriksdal.date,
        y=henriksdal_wwtp_henriksdal.value,
        mode="lines+markers",
        marker=dict(color=colours[8], size=7),
        marker_symbol="diamond",
        line=dict(color=colours[8], width=2),
    )
)

fig.add_trace(
    go.Scatter(
        name="Henriksdal, Sickla Inlet",
        x=henriksdal_wwtp_sickla.date,
        y=henriksdal_wwtp_sickla.value,
        mode="lines+markers",
        marker=dict(color=colours[9], size=7),
        marker_symbol="triangle-down",
        line=dict(color=colours[9], width=2),
    )
)

fig.add_trace(
    go.Scatter(
        name="Käppala",
        x=kappala_wwtp.date,
        y=kappala_wwtp.value,
        mode="lines+markers",
        marker=dict(color=colours[10], size=7),
        marker_symbol="hourglass",
        line=dict(color=colours[10], width=2),
    )
)

fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=14),
    margin=dict(r=150, t=65, b=0, l=0),
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.99, font=dict(size=16)),
    hovermode="x unified",
    hoverdistance=1,
    hoverlabel_namelength=-1,
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
    range=[min_date, max_date],
)
fig.update_yaxes(
    title="<b>N3-gene copy number per<br>PMMoV gene copy number x 10<sup>4</sup></b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
    zeroline=True,
    zerolinecolor="black",
    # Below will set the y-axis range to constant, if you wish
    range=[0, max(wastewater_data_res["value"] * 1.15)],
)

fig.update_layout(
    updatemenus=[
        dict(
            buttons=list(
                [
                    dict(
                        label="Reselect all areas",
                        method="update",
                        args=[
                            {"visible": [True]},
                        ],
                    ),
                    dict(
                        label="Deselect all areas",
                        method="update",
                        args=[
                            {"visible": "legendonly"},
                        ],
                    ),
                ]
            ),
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=1.1,
            xanchor="left",
            y=1.1,
            yanchor="top",
        ),
        dict(
            buttons=list(
                [
                    dict(
                        label="Last 16 weeks",
                        method="relayout",
                        args=[
                            {
                                "xaxis.range": (
                                    min(wastewater_data_res.date),
                                    max(wastewater_data_res.date),
                                ),
                                "yaxis.range": (
                                    min(wastewater_data_res.value),
                                    (max(wastewater_data_res.value) * 1.15),
                                ),
                            },
                        ],
                    ),
                    dict(
                        label="Whole timeline",
                        method="relayout",
                        args=[
                            {
                                "xaxis.range": (
                                    min(wastewater_data.date),
                                    max(wastewater_data.date),
                                ),
                                "yaxis.range": (
                                    min(wastewater_data.value),
                                    (max(wastewater_data.value) * 1.15),
                                ),
                            },
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
            y=1.1,
            yanchor="top",
        ),
    ]
)

# Below can show figure locally in tests
fig.show()

# Below prints as html
# fig.write_html(
#     "wastewater_combined_stockholm.html", include_plotlyjs=True, full_html=True)

# Prints as a json file
fig.write_json("wastewater_combined_stockholm_new.json")

# Below can produce a static image
# fig.write_image("wastewater_combined_graph.png")

# print(fig.to_json())
