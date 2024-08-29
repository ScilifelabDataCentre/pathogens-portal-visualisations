import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from plotly.io import write_image

# # Knivsta, Vaxholm and Österåker.
# Göteborg, Malmö and Stockholm-Käppala

wastewater_data = pd.read_csv(
    "https://blobserver.dc.scilifelab.se/blob/SLU_wastewater_data.csv",
    sep=",",
)
wastewater_data["year"] = (wastewater_data["week"].str[:4]).astype(int)
wastewater_data["week_no"] = wastewater_data["week"].str[-3:]
wastewater_data["week_no"] = wastewater_data["week_no"].str.replace("*", "")
wastewater_data["week_no"] = wastewater_data["week_no"].str.replace("-", "").astype(int)
# set the date to the start of the week (Monday)
wastewater_data["day"] = 1
wastewater_data["date"] = wastewater_data.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)

# Only data after week 47 2022
wastewater_data = wastewater_data[(wastewater_data["date"] >= "2023-03-20")]
wastewater_data.rename(
    columns={
        # "infA-gene cn per PMMoV cn x 10000": "influenza",
        "infB/PMMoV x 1000": "influenza_b",
    },
    inplace=True,
)

# below line is only needed until 'ND' and 'D' tags begin to be added
wastewater_data["influenza_b"] = wastewater_data["influenza_b"].astype(str)

# Below sets up having 'ND' and 'D' shown, so it's possible to show when there is a sample, but it is below detection or quantification limits, respectively
wastewater_data["detection"] = np.where(
    wastewater_data.influenza_b.str.contains("\\d"), np.nan, wastewater_data.influenza_b
)

wastewater_data["influenza_b"] = wastewater_data["influenza_b"].str.replace(
    "ND", "0", regex=True
)
wastewater_data["influenza_b"] = (
    wastewater_data["influenza_b"].str.replace("D", "0", regex=True).astype(float)
)

# print(wastewater_data.info())


# Below sets a dataset for each city. Need to add to it if more places are added
# Will also need to add in a go.Scatter trace in the fig (no change needed to layout)
# wastewater_Ekerö = wastewater_data[(wastewater_data["channel"] == "Ekerö")]
# wastewater_Enköping = wastewater_data[(wastewater_data["channel"] == "Enköping")]
wastewater_Gävle = wastewater_data[(wastewater_data["channel"] == "Gävle")]
wastewater_Göteborg = wastewater_data[(wastewater_data["channel"] == "Göteborg")]
wastewater_Helsingborg = wastewater_data[(wastewater_data["channel"] == "Helsingborg")]
wastewater_Jönköping = wastewater_data[(wastewater_data["channel"] == "Jönköping")]
wastewater_Karlstad = wastewater_data[(wastewater_data["channel"] == "Karlstad")]
wastewater_Kalmar = wastewater_data[(wastewater_data["channel"] == "Kalmar")]
# wastewater_Knivsta = wastewater_data[(wastewater_data["channel"] == "Knivsta")]
wastewater_Linköping = wastewater_data[(wastewater_data["channel"] == "Linköping")]
wastewater_Luleå = wastewater_data[(wastewater_data["channel"] == "Luleå")]
wastewater_Malmö = wastewater_data[(wastewater_data["channel"] == "Malmö")]
wastewater_StockholmBromma = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Bromma")
]
wastewater_StockholmGrödinge = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Grödinge")
]
wastewater_StockholmHenriksdal = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Henriksdal")
]
wastewater_StockholmKäppala = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Käppala")
]
# wastewater_Tierp = wastewater_data[(wastewater_data["channel"] == "Tierp")]
wastewater_Umeå = wastewater_data[(wastewater_data["channel"] == "Umeå")]
wastewater_Uppsala = wastewater_data[(wastewater_data["channel"] == "Uppsala")]
wastewater_Västerås = wastewater_data[(wastewater_data["channel"] == "Västerås")]
# wastewater_Vaxholm = wastewater_data[(wastewater_data["channel"] == "Vaxholm")]
# wastewater_Älvkarleby = wastewater_data[(wastewater_data["channel"] == "Älvkarleby")]
wastewater_Örebro = wastewater_data[(wastewater_data["channel"] == "Örebro")]
wastewater_Östersund = wastewater_data[(wastewater_data["channel"] == "Östersund")]
# wastewater_Österåker = wastewater_data[(wastewater_data["channel"] == "Österåker")]
wastewater_Östhammar = wastewater_data[(wastewater_data["channel"] == "Östhammar")]

# original column - infA-gene cn per PMMoV cn x 10000

fig = go.Figure(
    data=[
        go.Scatter(
            name="Gävle",
            x=wastewater_Gävle.date,
            y=wastewater_Gävle.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[2], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[2], width=2),
            customdata=wastewater_Gävle["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Gävle["detection"] == "ND",
                    wastewater_Gävle["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Göteborg",
            x=wastewater_Göteborg.date,
            y=wastewater_Göteborg.influenza_b,
            mode="lines+markers",
            marker=dict(color="#9400d3", size=7),
            marker_symbol="cross",
            line=dict(color="#9400d3", width=2),
            customdata=wastewater_Göteborg["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Göteborg["detection"] == "ND",
                    wastewater_Göteborg["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Helsingborg",
            x=wastewater_Helsingborg.date,
            y=wastewater_Helsingborg.influenza_b,
            mode="lines+markers",
            marker=dict(color="#EFB261", size=7),
            marker_symbol="square",
            line=dict(color="#EFB261", width=2),
            customdata=wastewater_Helsingborg["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Helsingborg["detection"] == "ND",
                    wastewater_Helsingborg["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Jönköping",
            x=wastewater_Jönköping.date,
            y=wastewater_Jönköping.influenza_b,
            mode="lines+markers",
            marker=dict(color="#FFA500", size=7),
            marker_symbol="cross",
            line=dict(color="#FFA500", width=2),
            customdata=wastewater_Jönköping["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Jönköping["detection"] == "ND",
                    wastewater_Jönköping["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Karlstad",
            x=wastewater_Karlstad.date,
            y=wastewater_Karlstad.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[0], size=7),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[0], width=2),
            customdata=wastewater_Karlstad["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Karlstad["detection"] == "ND",
                    wastewater_Karlstad["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Kalmar",
            x=wastewater_Kalmar.date,
            y=wastewater_Kalmar.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[3], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[3], width=2),
            customdata=wastewater_Kalmar["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Kalmar["detection"] == "ND",
                    wastewater_Kalmar["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Linköping",
            x=wastewater_Linköping.date,
            y=wastewater_Linköping.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[1], size=7),
            marker_symbol="cross",
            line=dict(color=px.colors.diverging.RdBu[1], width=2),
            customdata=wastewater_Linköping["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Linköping["detection"] == "ND",
                    wastewater_Linköping["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Luleå",
            x=wastewater_Luleå.date,
            y=wastewater_Luleå.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[9], size=7),
            marker_symbol="cross",
            line=dict(color=px.colors.diverging.RdBu[9], width=2),
            customdata=wastewater_Luleå["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Luleå["detection"] == "ND",
                    wastewater_Luleå["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Malmö",
            x=wastewater_Malmö.date,
            y=wastewater_Malmö.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[8], size=7),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[8], width=2),
            customdata=wastewater_Malmö["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Malmö["detection"] == "ND",
                    wastewater_Malmö["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Stockholm-Bromma",
            x=wastewater_StockholmBromma.date,
            y=wastewater_StockholmBromma.influenza_b,
            mode="lines+markers",
            marker=dict(color="black", size=7),
            marker_symbol="cross",
            line=dict(color="black", width=2),
            customdata=wastewater_StockholmBromma["detection"],
            hovertemplate=np.select(
                [
                    wastewater_StockholmBromma["detection"] == "ND",
                    wastewater_StockholmBromma["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Stockholm-Grödinge",
            x=wastewater_StockholmGrödinge.date,
            y=wastewater_StockholmGrödinge.influenza_b,
            mode="lines+markers",
            marker=dict(color="#ff00ff", size=7),
            marker_symbol="square",
            line=dict(color="#ff00ff", width=2),
            customdata=wastewater_StockholmGrödinge["detection"],
            hovertemplate=np.select(
                [
                    wastewater_StockholmGrödinge["detection"] == "ND",
                    wastewater_StockholmGrödinge["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Stockholm-Henriksdal",
            x=wastewater_StockholmHenriksdal.date,
            y=wastewater_StockholmHenriksdal.influenza_b,
            mode="lines+markers",
            marker=dict(color="#4ADEDE", size=7),
            marker_symbol="cross",
            line=dict(color="#4ADEDE", width=2),
            customdata=wastewater_StockholmHenriksdal["detection"],
            hovertemplate=np.select(
                [
                    wastewater_StockholmHenriksdal["detection"] == "ND",
                    wastewater_StockholmHenriksdal["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Stockholm-Käppala",
            x=wastewater_StockholmKäppala.date,
            y=wastewater_StockholmKäppala.influenza_b,
            mode="lines+markers",
            marker=dict(color="gold", size=7),
            marker_symbol="square",
            line=dict(color="gold", width=2),
            customdata=wastewater_StockholmKäppala["detection"],
            hovertemplate=np.select(
                [
                    wastewater_StockholmKäppala["detection"] == "ND",
                    wastewater_StockholmKäppala["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Umeå",
            x=wastewater_Umeå.date,
            y=wastewater_Umeå.influenza_b,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[10], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[10], width=2),
            customdata=wastewater_Umeå["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Umeå["detection"] == "ND",
                    wastewater_Umeå["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Uppsala",
            x=wastewater_Uppsala.date,
            y=wastewater_Uppsala.influenza_b,
            mode="lines+markers",
            marker=dict(color="#663399", size=7),
            marker_symbol="square",
            line=dict(color="#663399", width=2),
            customdata=wastewater_Uppsala["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Uppsala["detection"] == "ND",
                    wastewater_Uppsala["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Västerås",
            x=wastewater_Västerås.date,
            y=wastewater_Västerås.influenza_b,
            mode="lines+markers",
            marker=dict(color="#B691d2", size=7),
            marker_symbol="hourglass",
            line=dict(color="#B691d2", width=2),
            customdata=wastewater_Västerås["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Västerås["detection"] == "ND",
                    wastewater_Västerås["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Örebro",
            x=wastewater_Örebro.date,
            y=wastewater_Örebro.influenza_b,
            mode="lines+markers",
            marker=dict(color="darkgoldenrod", size=7),
            marker_symbol="square",
            line=dict(color="darkgoldenrod", width=2),
            customdata=wastewater_Örebro["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Örebro["detection"] == "ND",
                    wastewater_Örebro["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Östersund",
            x=wastewater_Östersund.date,
            y=wastewater_Östersund.influenza_b,
            mode="lines+markers",
            marker=dict(color="#997950", size=7),
            marker_symbol="hourglass",
            line=dict(color="#997950", width=2),
            customdata=wastewater_Östersund["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Östersund["detection"] == "ND",
                    wastewater_Östersund["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
        go.Scatter(
            name="Östhammar",
            x=wastewater_Östhammar.date,
            y=wastewater_Östhammar.influenza_b,
            mode="lines+markers",
            marker=dict(color="lightslategray", size=7),
            marker_symbol="hourglass",
            line=dict(color="lightslategray", width=2),
            customdata=wastewater_Östhammar["detection"],
            hovertemplate=np.select(
                [
                    wastewater_Östhammar["detection"] == "ND",
                    wastewater_Östhammar["detection"] == "D",
                ],
                ["%{customdata}", "%{customdata}"],
                "%{y:.2f}",
            ),
        ),
    ]
)
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=14),
    margin=dict(r=150, t=65, b=0, l=0),
    # width=900,
    # height=500,
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.99, font=dict(size=14)),
    hovermode="x unified",
    hoverdistance=1,
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
    hoverformat="%b %d, %Y (week %V)",
)
fig.update_yaxes(
    title="<b>infB/PMMoV x 1000</b>",
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
        )
    ]
)
# Below can show figure locally in tests
# fig.show()

# Below prints as html
# fig.write_html(
#    "wastewater_combined_slu_regular.html", include_plotlyjs=True, full_html=True
# )

# Prints as a json file
# fig.write_json("wastewater_slu_infB.json")

# Below can produce a static image
# fig.write_image("wastewater_combined_graph.png")

print(fig.to_json())
