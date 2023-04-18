import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from plotly.io import write_image

# # Knivsta, Vaxholm and Österåker.
# Göteborg, Malmö and Stockholm-Käppala

wastewater_data = pd.read_csv(
    "/Users/liahu895/Documents/GitHub/covid-portal-visualisations/wastewater/data/SARS-Cov-2-N1_infA quantification data_10-2023_corr.csv",
    # "https://datagraphics.dckube.scilifelab.se/api/dataset/0ac8fa02871745048491de74e5689da9.csv",
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

# Only data after week 47 2022
wastewater_data = wastewater_data[(wastewater_data["date"] >= "2022-10-17")]

# Below sets a dataset for each city. Need to add to it if more places are added
# Will also need to add in a go.Scatter trace in the fig (no change needed to layout)
wastewater_Ekerö = wastewater_data[(wastewater_data["channel"] == "Ekerö")]
wastewater_Enköping = wastewater_data[(wastewater_data["channel"] == "Enköping")]
wastewater_Gävle = wastewater_data[(wastewater_data["channel"] == "Gävle")]
wastewater_Göteborg = wastewater_data[(wastewater_data["channel"] == "Göteborg")]  ##new
wastewater_Helsingborg = wastewater_data[(wastewater_data["channel"] == "Helsingborg")]
wastewater_Jönköping = wastewater_data[(wastewater_data["channel"] == "Jönköping")]
wastewater_Kalmar = wastewater_data[(wastewater_data["channel"] == "Kalmar")]
wastewater_Malmö = wastewater_data[(wastewater_data["channel"] == "Malmö")]  ##new
wastewater_StockholmKäppala = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Käppala")
]  ##new
# wastewater_Knivsta = wastewater_data[(wastewater_data["channel"] == "Knivsta")]
wastewater_Tierp = wastewater_data[(wastewater_data["channel"] == "Tierp")]
wastewater_Umeå = wastewater_data[(wastewater_data["channel"] == "Umeå")]
wastewater_Uppsala = wastewater_data[(wastewater_data["channel"] == "Uppsala")]
wastewater_Västerås = wastewater_data[(wastewater_data["channel"] == "Västerås")]
# wastewater_Vaxholm = wastewater_data[(wastewater_data["channel"] == "Vaxholm")]
wastewater_Älvkarleby = wastewater_data[(wastewater_data["channel"] == "Älvkarleby")]
wastewater_Örebro = wastewater_data[(wastewater_data["channel"] == "Örebro")]
wastewater_Östersund = wastewater_data[(wastewater_data["channel"] == "Östersund")]
# wastewater_Österåker = wastewater_data[(wastewater_data["channel"] == "Österåker")]
wastewater_Östhammar = wastewater_data[(wastewater_data["channel"] == "Östhammar")]

# original column - infA-gene cn per PMMoV cn x 10000

fig = go.Figure(
    data=[
        go.Scatter(
            name="Ekerö",
            x=wastewater_Ekerö.date,
            y=wastewater_Ekerö.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[0], size=7),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[0], width=2),
        ),
        go.Scatter(
            name="Enköping",
            x=wastewater_Enköping.date,
            y=wastewater_Enköping.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[1], size=7),
            marker_symbol="cross",
            line=dict(color=px.colors.diverging.RdBu[1], width=2),
        ),
        go.Scatter(
            name="Gävle",
            x=wastewater_Gävle.date,
            y=wastewater_Gävle.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[2], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[2], width=2),
        ),
        go.Scatter(  ##NEW!!
            name="Göteborg",
            x=wastewater_Göteborg.date,
            y=wastewater_Göteborg.influenza,
            mode="lines+markers",
            marker=dict(color="#9400d3", size=7),
            marker_symbol="cross",
            line=dict(color="#9400d3", width=2),
        ),
        go.Scatter(
            name="Helsingborg",
            x=wastewater_Helsingborg.date,
            y=wastewater_Helsingborg.influenza,
            mode="lines+markers",
            marker=dict(color="#EFB261", size=7),
            marker_symbol="square",
            line=dict(color="#EFB261", width=2),
        ),
        go.Scatter(
            name="Jönköping",
            x=wastewater_Jönköping.date,
            y=wastewater_Jönköping.influenza,
            mode="lines+markers",
            marker=dict(color="#FFA500", size=7),
            marker_symbol="cross",
            line=dict(color="#FFA500", width=2),
        ),
        go.Scatter(
            name="Kalmar",
            x=wastewater_Kalmar.date,
            y=wastewater_Kalmar.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[3], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[3], width=2),
        ),
        # go.Scatter(
        #     name="Knivsta",
        #     x=wastewater_Knivsta.date,
        #     y=wastewater_Knivsta.influenza,
        #     mode="lines+markers",
        #     marker=dict(color=px.colors.diverging.RdBu[8], size=7),
        #     marker_symbol="square",
        #     line=dict(color=px.colors.diverging.RdBu[8], width=2),
        # ),
        go.Scatter(  ##NEW
            name="Malmö",
            x=wastewater_Malmö.date,
            y=wastewater_Malmö.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[8], size=7),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[8], width=2),
        ),
        go.Scatter(  ##NEW
            name="Stockholm-Käppala",
            x=wastewater_StockholmKäppala.date,
            y=wastewater_StockholmKäppala.influenza,
            mode="lines+markers",
            marker=dict(color="gold", size=7),
            marker_symbol="square",
            line=dict(color="gold", width=2),
        ),
        go.Scatter(
            name="Tierp",
            x=wastewater_Tierp.date,
            y=wastewater_Tierp.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[9], size=7),
            marker_symbol="cross",
            line=dict(color=px.colors.diverging.RdBu[9], width=2),
        ),
        go.Scatter(
            name="Umeå",
            x=wastewater_Umeå.date,
            y=wastewater_Umeå.influenza,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[10], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[10], width=2),
        ),
        go.Scatter(
            name="Uppsala",
            x=wastewater_Uppsala.date,
            y=wastewater_Uppsala.influenza,
            mode="lines+markers",
            marker=dict(color="#663399", size=7),
            marker_symbol="square",
            line=dict(color="#663399", width=2),
        ),
        go.Scatter(
            name="Västerås",
            x=wastewater_Västerås.date,
            y=wastewater_Västerås.influenza,
            mode="lines+markers",
            marker=dict(color="#B691d2", size=7),
            marker_symbol="hourglass",
            line=dict(color="#B691d2", width=2),
        ),
        # go.Scatter(
        #     name="Vaxholm",
        #     x=wastewater_Vaxholm.date,
        #     y=wastewater_Vaxholm.influenza,
        #     mode="lines+markers",
        #     marker=dict(color="#9400d3", size=7),
        #     marker_symbol="cross",
        #     line=dict(color="#9400d3", width=2),
        # ),
        go.Scatter(
            name="Älvkarleby",
            x=wastewater_Älvkarleby.date,
            y=wastewater_Älvkarleby.influenza,
            mode="lines+markers",
            marker=dict(color="#ff00ff", size=7),
            marker_symbol="hourglass",
            line=dict(color="#ff00ff", width=2),
        ),
        go.Scatter(
            name="Örebro",
            x=wastewater_Örebro.date,
            y=wastewater_Örebro.influenza,
            mode="lines+markers",
            marker=dict(color="darkgoldenrod", size=7),
            marker_symbol="square",
            line=dict(color="darkgoldenrod", width=2),
        ),
        go.Scatter(
            name="Östersund",
            x=wastewater_Östersund.date,
            y=wastewater_Östersund.influenza,
            mode="lines+markers",
            marker=dict(color="#997950", size=7),
            marker_symbol="hourglass",
            line=dict(color="#997950", width=2),
        ),
        # go.Scatter(
        #     name="Österåker",
        #     x=wastewater_Österåker.date,
        #     y=wastewater_Österåker.influenza,
        #     mode="lines+markers",
        #     marker=dict(color="gold", size=7),
        #     marker_symbol="cross",
        #     line=dict(color="gold", width=2),
        # ),
        go.Scatter(
            name="Östhammar",
            x=wastewater_Östhammar.date,
            y=wastewater_Östhammar.influenza,
            mode="lines+markers",
            marker=dict(color="lightslategray", size=7),
            marker_symbol="hourglass",
            line=dict(color="lightslategray", width=2),
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
    title="<b>InfA-gene copy number per PMMOV<br>gene copy number x 10^4</b>",
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
fig.show()

# Below prints as html
# fig.write_html(
#    "wastewater_combined_slu_regular.html", include_plotlyjs=True, full_html=True
# )

# Prints as a json file
# fig.write_json("wastewater_combined_slu_regular.json")

# Below can produce a static image
# fig.write_image("wastewater_combined_graph.png")

# print(fig.to_json())
