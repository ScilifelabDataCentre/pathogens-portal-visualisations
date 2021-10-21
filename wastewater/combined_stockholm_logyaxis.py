import pandas as pd
import datetime
import plotly.graph_objects as go
from datetime import datetime as dt
from plotly.io import write_image


wastewater_data = pd.read_csv(
    "https://datagraphics.dckube.scilifelab.se/dataset/65f19e61386a4a039aa798010ca42469.csv",
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

print(wastewater_data)

# Below sets a dataset for each city. Need to add to it if more places are added
# Will also need to add in a go.Scatter trace in the fig (no change needed to layout)
bromma_wwtp_jarva = wastewater_data[
    (wastewater_data["wwtp"] == "Bromma WWTP, Järva Inlet")
]
bromma_wwtp_riksby = wastewater_data[
    (wastewater_data["wwtp"] == "Bromma WWTP, Riksby Inlet")
]
henriksdal_wwtp_hasselby = wastewater_data[
    (wastewater_data["wwtp"] == "Henriksdal WWTP, Hässelby Inlet")
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
            marker=dict(color="#F8ACF4"),
            line=dict(color="#F8ACF4", width=2),
        ),
        go.Scatter(
            name="Bromma, Riksby Inlet",
            x=bromma_wwtp_riksby.date,
            y=bromma_wwtp_riksby.value,
            mode="lines+markers",
            marker=dict(color="#308ACF"),
            line=dict(color="#308ACF", width=2),
        ),
        go.Scatter(
            name="Henriksdal, Hässelby Inlet",
            x=henriksdal_wwtp_hasselby.date,
            y=henriksdal_wwtp_hasselby.value,
            mode="lines+markers",
            # connectgaps=False,
            marker=dict(color="#9513E9"),
            line=dict(color="#9513E9", width=2),
        ),
        go.Scatter(
            name="Henriksdal, Henriksdal Inlet",
            x=henriksdal_wwtp_henriksdal.date,
            y=henriksdal_wwtp_henriksdal.value,
            mode="lines+markers",
            marker=dict(color="#FF3333"),
            line=dict(color="#FF3333", width=2),
        ),
        go.Scatter(
            name="Henriksdal, Sickla Inlet",
            x=henriksdal_wwtp_sickla.date,
            y=henriksdal_wwtp_sickla.value,
            mode="lines+markers",
            marker=dict(color="#E98B13"),
            line=dict(color="#E98B13", width=2),
        ),
        go.Scatter(
            name="Käppala",
            x=kappala_wwtp.date,
            y=kappala_wwtp.value,
            mode="lines+markers",
            marker=dict(color="#045C64"),
            line=dict(color="#045C64", width=2),
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
    title="<b>Relative copy number of<br>SARS-CoV-2 to PPMMoV, log</b>",
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
                        label="Reset selected inlets",
                        method="update",
                        args=[
                            {"visible": [True]},
                            # {"title": "", "annotations": []},
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
#fig.write_html(
#    "wastewater_combined_stockholm_logyaxis.html", include_plotlyjs=True, full_html=True)
# Prints as a json file
fig.write_json("wastewater_stockholm_logyaxis.json")
# Below can produce a static image
# fig.write_image("wastewater_combined_graph.png")
