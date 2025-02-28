import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from plotly.io import write_image

# datagraphics is shut down, raw data is moved to blobserver, generate csv from it
# https://blobserver.dc.scilifelab.se/blob/stockholm_wastewater_method_Sep_2021.xlsx/info
wastewater_data = pd.read_csv(
    "https://datagraphics.dc.scilifelab.se/api/dataset/65f19e61386a4a039aa798010ca42469.csv",
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

# Restrict data to only 2021 for the purpose of this plot
wastewater_data = wastewater_data[(wastewater_data["year"] > 2020)]

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

fig = go.Figure(
    data=[
        go.Scatter(
            name="Bromma, Järva Inlet",
            x=bromma_wwtp_jarva.date,
            y=bromma_wwtp_jarva.value,
            mode="lines+markers",
            marker=dict(color=colours[0], size=7),
            marker_symbol="square",
            line=dict(color=colours[0], width=2),
        ),
        go.Scatter(
            name="Bromma, Riksby Inlet",
            x=bromma_wwtp_riksby.date,
            y=bromma_wwtp_riksby.value,
            mode="lines+markers",
            marker=dict(color=colours[1], size=7),
            marker_symbol="circle",
            line=dict(color=colours[1], width=2),
        ),
        go.Scatter(
            name="Bromma, Hässelby Inlet",
            x=bromma_wwtp_hasselby.date,
            y=bromma_wwtp_hasselby.value,
            mode="lines+markers",
            marker=dict(color=colours[3], size=7),
            marker_symbol="x",
            line=dict(color=colours[3], width=2),
        ),
        go.Scatter(
            name="Henriksdal, Henriksdal Inlet",
            x=henriksdal_wwtp_henriksdal.date,
            y=henriksdal_wwtp_henriksdal.value,
            mode="lines+markers",
            marker=dict(color=colours[8], size=7),
            marker_symbol="diamond",
            line=dict(color=colours[8], width=2),
        ),
        go.Scatter(
            name="Henriksdal, Sickla Inlet",
            x=henriksdal_wwtp_sickla.date,
            y=henriksdal_wwtp_sickla.value,
            mode="lines+markers",
            marker=dict(color=colours[9], size=7),
            marker_symbol="triangle-down",
            line=dict(color=colours[9], width=2),
        ),
        go.Scatter(
            name="Käppala",
            x=kappala_wwtp.date,
            y=kappala_wwtp.value,
            mode="lines+markers",
            marker=dict(color=colours[10], size=7),
            marker_symbol="hourglass",
            line=dict(color=colours[10], width=2),
        ),
    ]
)
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=14),
    margin=dict(r=150, t=65, b=0, l=0),
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.99, font=dict(size=16)),
    hovermode="x unified",
    hoverdistance=1,
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
)
fig.update_yaxes(
    title="<b>N3-gene copy number per<br>PMMoV gene copy number x 10^4, log</b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
    zeroline=True,
    zerolinecolor="black",
    type="log"
    # Below will set the y-axis range to constant, if you wish
    # range=[0, max(wastewater_data["relative_copy_number"] * 1.15)],
)
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=1.1,
            y=1.1,
            xanchor="right",
            yanchor="top",
            buttons=list(
                [
                    dict(
                        label="Reselect all areas",
                        method="update",
                        args=[
                            {"visible": [True]},
                            # {"title": "", "annotations": []},
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
        )
    ]
)
# Below can show figure locally in tests
# fig.show()

# Below prints as html
# fig.write_html(
#    "wastewater_combined_stockholm_logyaxis.html", include_plotlyjs=True, full_html=True)

# Prints as a json file
# fig.write_json("wastewater_stockholm_logyaxis.json")

# Below can produce a static image
# fig.write_image("wastewater_combined_graph.png")

print(fig.to_json())
