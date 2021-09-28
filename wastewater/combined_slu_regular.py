import pandas as pd
import datetime
import plotly.graph_objects as go
from datetime import datetime as dt


wastewater_data = pd.read_csv(
    "https://datagraphics.dckube.scilifelab.se/dataset/0ac8fa02871745048491de74e5689da9.csv",
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
# Below sets a dataset for each city. Need to add to it if more places are added
# Will also need to add in a go.Scatter trace in the fig (no change needed to layout)
wastewater_Ekerö = wastewater_data[(wastewater_data["channel"] == "Ekerö")]
wastewater_Enköping = wastewater_data[(wastewater_data["channel"] == "Enköping")]
wastewater_Kalmar = wastewater_data[(wastewater_data["channel"] == "Kalmar")]
wastewater_Knivsta = wastewater_data[(wastewater_data["channel"] == "Knivsta")]
wastewater_Tierp = wastewater_data[(wastewater_data["channel"] == "Tierp")]
wastewater_Umeå = wastewater_data[(wastewater_data["channel"] == "Umeå")]
wastewater_Uppsala = wastewater_data[(wastewater_data["channel"] == "Uppsala")]
wastewater_Vaxholm = wastewater_data[(wastewater_data["channel"] == "Vaxholm")]
wastewater_Älvkarleby = wastewater_data[(wastewater_data["channel"] == "Älvkarleby")]
wastewater_Örebro = wastewater_data[(wastewater_data["channel"] == "Örebro")]
wastewater_Österåker = wastewater_data[(wastewater_data["channel"] == "Österåker")]
wastewater_Östhammar = wastewater_data[(wastewater_data["channel"] == "Östhammar")]

fig = go.Figure(
    data=[
        go.Scatter(
            name="Ekerö",
            x=wastewater_Ekerö.date,
            y=wastewater_Ekerö.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#F8ACF4"),
            line=dict(color="#F8ACF4", width=2),
        ),
        go.Scatter(
            name="Enköping",
            x=wastewater_Enköping.date,
            y=wastewater_Enköping.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#308ACF"),
            line=dict(color="#308ACF", width=2),
        ),
        go.Scatter(
            name="Kalmar",
            x=wastewater_Kalmar.date,
            y=wastewater_Kalmar.relative_copy_number,
            mode="lines+markers",
            # connectgaps=False,
            marker=dict(color="#9513E9"),
            line=dict(color="#9513E9", width=2),
        ),
        go.Scatter(
            name="Knivsta",
            x=wastewater_Knivsta.date,
            y=wastewater_Knivsta.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#FF3333"),
            line=dict(color="#FF3333", width=2),
        ),
        go.Scatter(
            name="Tierp",
            x=wastewater_Tierp.date,
            y=wastewater_Tierp.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#E98B13"),
            line=dict(color="#E98B13", width=2),
        ),
        go.Scatter(
            name="Umeå",
            x=wastewater_Umeå.date,
            y=wastewater_Umeå.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#045C64"),
            line=dict(color="#045C64", width=2),
        ),
        go.Scatter(
            name="Uppsala",
            x=wastewater_Uppsala.date,
            y=wastewater_Uppsala.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#491F53"),
            line=dict(color="#491F53", width=2),
        ),
        go.Scatter(
            name="Vaxholm",
            x=wastewater_Vaxholm.date,
            y=wastewater_Vaxholm.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#FBEA1C"),
            line=dict(color="#FBEA1C", width=2),
        ),
        go.Scatter(
            name="Älvkarleby",
            x=wastewater_Älvkarleby.date,
            y=wastewater_Älvkarleby.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#1CFBB2"),
            line=dict(color="#1CFBB2", width=2),
        ),
        go.Scatter(
            name="Örebro",
            x=wastewater_Örebro.date,
            y=wastewater_Örebro.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#A7C947"),
            line=dict(color="#A7C947", width=2),
        ),
        go.Scatter(
            name="Österåker",
            x=wastewater_Österåker.date,
            y=wastewater_Österåker.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#10077F"),
            line=dict(color="#10077F", width=2),
        ),
        go.Scatter(
            name="Östhammar",
            x=wastewater_Östhammar.date,
            y=wastewater_Östhammar.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#BEBBC0"),
            line=dict(color="#BEBBC0", width=2),
        ),
    ]
)
fig.update_layout(
    plot_bgcolor="white",
    autosize=False,
    font=dict(size=14),
    margin=dict(r=150, t=65, b=0, l=0),
    # width=900,
    # height=500,
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
    title="<b>Relative copy number of<br>SARS-CoV-2 to PPMMoV (%)</b><br>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
    zeroline=True,
    zerolinecolor="black",
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
                        label="Reset",
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
# fig.show()#renderer="json")
fig.write_json("wastewater_test.json")
# Below prints as html
# fig.write_html(
#     "wastewater_combined_slu_regular.html", include_plotlyjs=False, full_html=False
# )
# Below can produce a static image
# fig.write_image("wastewater_combined_graph.png")
