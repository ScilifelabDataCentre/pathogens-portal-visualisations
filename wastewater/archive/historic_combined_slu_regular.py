import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from plotly.io import write_image

# # Knivsta, Vaxholm and Österåker.
# Göteborg, Malmö and Stockholm-Käppala

wastewater_data = pd.read_csv(
    "https://blobserver.dc.scilifelab.se/blob/historic_SLU_wastewater_data.csv",
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
# The below accomodates a change in the column title for the COVID data
wastewater_data.rename(
    columns={
        "SARS-CoV2/PMMoV x 1000": "relative_copy_number",
    },
    inplace=True,
)

# Below sets a dataset for each city. Need to add to it if more places are added
# Will also need to add in a go.Scatter trace in the fig (no change needed to layout)
# wastewater_Ekerö = wastewater_data[(wastewater_data["channel"] == "Ekerö")]
# wastewater_Enköping = wastewater_data[(wastewater_data["channel"] == "Enköping")]
wastewater_Gävle = wastewater_data[(wastewater_data["channel"] == "Gävle")]
wastewater_Göteborg = wastewater_data[(wastewater_data["channel"] == "Göteborg")]  ##new
wastewater_Helsingborg = wastewater_data[(wastewater_data["channel"] == "Helsingborg")]
wastewater_Jönköping = wastewater_data[(wastewater_data["channel"] == "Jönköping")]
wastewater_Kalmar = wastewater_data[(wastewater_data["channel"] == "Kalmar")]
wastewater_Karlstad = wastewater_data[
    (wastewater_data["channel"] == "Karlstad")
]  # added 2023-06-12
wastewater_Linköping = wastewater_data[
    (wastewater_data["channel"] == "Linköping")
]  # added 2023-06-12
wastewater_Luleå = wastewater_data[
    (wastewater_data["channel"] == "Luleå")
]  # added 2023-06-12
wastewater_Malmö = wastewater_data[(wastewater_data["channel"] == "Malmö")]  ##new
wastewater_StockholmBromma = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Bromma")
]  # added 2023-07-04
wastewater_StockholmGrödinge = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Grödinge")
]  # added 2023-06-12
wastewater_StockholmHenriksdal = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Henriksdal")
]  # added 2023-07-04
wastewater_StockholmKäppala = wastewater_data[
    (wastewater_data["channel"] == "Stockholm-Käppala")
]  ##new
# wastewater_Knivsta = wastewater_data[(wastewater_data["channel"] == "Knivsta")]
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

fig = go.Figure(
    data=[
        # go.Scatter(
        #     name="Ekerö",
        #     x=wastewater_Ekerö.date,
        #     y=wastewater_Ekerö.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color=px.colors.diverging.RdBu[0], size=7),
        #     marker_symbol="square",
        #     line=dict(color=px.colors.diverging.RdBu[0], width=2),
        # ),
        # go.Scatter(
        #     name="Enköping",
        #     x=wastewater_Enköping.date,
        #     y=wastewater_Enköping.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color=px.colors.diverging.RdBu[1], size=7),
        #     marker_symbol="cross",
        #     line=dict(color=px.colors.diverging.RdBu[1], width=2),
        # ),
        go.Scatter(
            name="Gävle",
            x=wastewater_Gävle.date,
            y=wastewater_Gävle.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[2], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[2], width=2),
        ),
        go.Scatter(  ##NEW!!
            name="Göteborg",
            x=wastewater_Göteborg.date,
            y=wastewater_Göteborg.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#9400d3", size=7),
            marker_symbol="cross",
            line=dict(color="#9400d3", width=2),
        ),
        go.Scatter(
            name="Helsingborg",
            x=wastewater_Helsingborg.date,
            y=wastewater_Helsingborg.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#EFB261", size=7),
            marker_symbol="square",
            line=dict(color="#EFB261", width=2),
        ),
        go.Scatter(
            name="Jönköping",
            x=wastewater_Jönköping.date,
            y=wastewater_Jönköping.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#FFA500", size=7),
            marker_symbol="cross",
            line=dict(color="#FFA500", width=2),
        ),
        go.Scatter(
            name="Kalmar",
            x=wastewater_Kalmar.date,
            y=wastewater_Kalmar.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[3], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[3], width=2),
        ),
        go.Scatter(  # added 2023-06-12
            name="Karlstad",
            x=wastewater_Karlstad.date,
            y=wastewater_Karlstad.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[0], size=7),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[0], width=2),
        ),
        go.Scatter(  # added 2023-06-12
            name="Linköping",
            x=wastewater_Linköping.date,
            y=wastewater_Linköping.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[1], size=7),
            marker_symbol="cross",
            line=dict(color=px.colors.diverging.RdBu[1], width=2),
        ),
        go.Scatter(  # added 2023-06-12
            name="Luleå",
            x=wastewater_Luleå.date,
            y=wastewater_Luleå.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[9], size=7),
            marker_symbol="cross",
            line=dict(color=px.colors.diverging.RdBu[9], width=2),
        ),
        # go.Scatter(
        #     name="Knivsta",
        #     x=wastewater_Knivsta.date,
        #     y=wastewater_Knivsta.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color=px.colors.diverging.RdBu[8], size=7),
        #     marker_symbol="square",
        #     line=dict(color=px.colors.diverging.RdBu[8], width=2),
        # ),
        go.Scatter(  ##NEW
            name="Malmö",
            x=wastewater_Malmö.date,
            y=wastewater_Malmö.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[8], size=7),
            marker_symbol="square",
            line=dict(color=px.colors.diverging.RdBu[8], width=2),
        ),
        go.Scatter(  # added 2023-07-04
            name="Stockholm-Bromma",
            x=wastewater_StockholmBromma.date,
            y=wastewater_StockholmBromma.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="black", size=7),
            marker_symbol="cross",
            line=dict(color="black", width=2),
        ),
        go.Scatter(  # added 2023-06-12
            name="Stockholm-Grödinge",
            x=wastewater_StockholmGrödinge.date,
            y=wastewater_StockholmGrödinge.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#ff00ff", size=7),
            marker_symbol="square",
            line=dict(color="#ff00ff", width=2),
        ),
        go.Scatter(  # added 2023-07-04
            name="Stockholm-Henriksdal",
            x=wastewater_StockholmHenriksdal.date,
            y=wastewater_StockholmHenriksdal.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#4ADEDE", size=7),
            marker_symbol="cross",
            line=dict(color="#4ADEDE", width=2),
        ),
        go.Scatter(  ##NEW
            name="Stockholm-Käppala",
            x=wastewater_StockholmKäppala.date,
            y=wastewater_StockholmKäppala.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="gold", size=7),
            marker_symbol="square",
            line=dict(color="gold", width=2),
        ),
        # go.Scatter(
        #     name="Tierp",
        #     x=wastewater_Tierp.date,
        #     y=wastewater_Tierp.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color=px.colors.diverging.RdBu[9], size=7),
        #     marker_symbol="cross",
        #     line=dict(color=px.colors.diverging.RdBu[9], width=2),
        # ),
        go.Scatter(
            name="Umeå",
            x=wastewater_Umeå.date,
            y=wastewater_Umeå.relative_copy_number,
            mode="lines+markers",
            marker=dict(color=px.colors.diverging.RdBu[10], size=7),
            marker_symbol="hourglass",
            line=dict(color=px.colors.diverging.RdBu[10], width=2),
        ),
        go.Scatter(
            name="Uppsala",
            x=wastewater_Uppsala.date,
            y=wastewater_Uppsala.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#663399", size=7),
            marker_symbol="square",
            line=dict(color="#663399", width=2),
        ),
        go.Scatter(
            name="Västerås",
            x=wastewater_Västerås.date,
            y=wastewater_Västerås.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#B691d2", size=7),
            marker_symbol="hourglass",
            line=dict(color="#B691d2", width=2),
        ),
        # go.Scatter(
        #     name="Vaxholm",
        #     x=wastewater_Vaxholm.date,
        #     y=wastewater_Vaxholm.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color="#9400d3", size=7),
        #     marker_symbol="cross",
        #     line=dict(color="#9400d3", width=2),
        # ),
        # go.Scatter(
        #     name="Älvkarleby",
        #     x=wastewater_Älvkarleby.date,
        #     y=wastewater_Älvkarleby.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color="#ff00ff", size=7),
        #     marker_symbol="hourglass",
        #     line=dict(color="#ff00ff", width=2),
        # ),
        go.Scatter(
            name="Örebro",
            x=wastewater_Örebro.date,
            y=wastewater_Örebro.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="darkgoldenrod", size=7),
            marker_symbol="square",
            line=dict(color="darkgoldenrod", width=2),
        ),
        go.Scatter(
            name="Östersund",
            x=wastewater_Östersund.date,
            y=wastewater_Östersund.relative_copy_number,
            mode="lines+markers",
            marker=dict(color="#997950", size=7),
            marker_symbol="hourglass",
            line=dict(color="#997950", width=2),
        ),
        # go.Scatter(
        #     name="Österåker",
        #     x=wastewater_Österåker.date,
        #     y=wastewater_Österåker.relative_copy_number,
        #     mode="lines+markers",
        #     marker=dict(color="gold", size=7),
        #     marker_symbol="cross",
        #     line=dict(color="gold", width=2),
        # ),
        go.Scatter(
            name="Östhammar",
            x=wastewater_Östhammar.date,
            y=wastewater_Östhammar.relative_copy_number,
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
    margin=dict(r=0, t=100, b=0, l=0),
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
    hoverformat="%b %d, %Y (week %W)",
)
fig.update_yaxes(
    title="<b>SARS-CoV-2/PMMoV x 1000</b>",
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
            # direction="right",
            active=0,
            x=1.2,
            y=1.15,
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

# Below save as html
# fig.write_html(
#    "wastewater_combined_slu_regular.html", include_plotlyjs=True, full_html=True
# )

# Saves as a json file
# fig.write_json("wastewater_combined_slu_regular.json")

print(fig.to_json())
