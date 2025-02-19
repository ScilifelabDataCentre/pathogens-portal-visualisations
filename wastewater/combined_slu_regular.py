import pandas as pd
import plotly.graph_objects as go

# Helper function that is later used
def get_plot_data(data, info):
    return [d[info] for d in data]

# Colour and shape info for the cities
cities_graph_info = {
    "Gavle": {"colour": "#d6604d", "symbol": "hourglass"},
    "Goteborg": {"colour": "#9400d3", "symbol": "cross"},
    "Helsingborg": {"colour": "#efb261", "symbol": "square"},
    "Jonkoping": {"colour": "#ffa500", "symbol": "cross"},
    "Kalmar": {"colour": "#f4a582", "symbol": "hourglass"},
    "Karlstad": {"colour": "#67001f", "symbol": "square"},
    "Linkoping": {"colour": "#b2182b", "symbol": "cross"},
    "Lulea": {"colour": "#2166ac", "symbol": "cross"},
    "Malmo": {"colour": "#4393c3", "symbol": "square"},
    "Orebro": {"colour": "#b8860b", "symbol": "square"},
    "Ostersund": {"colour": "#997950", "symbol": "hourglass"},
    "Osthammar": {"colour": "#778899", "symbol": "hourglass"},
    "Stockholm-Bromma": {"colour": "#000000", "symbol": "cross"},
    "Stockholm-Grodinge": {"colour": "#ff00ff", "symbol": "square"},
    "Stockholm-Henriksdal": {"colour": "#4adede", "symbol": "cross"},
    "Stockholm-Kappala": {"colour": "#ffd700", "symbol": "square"},
    "Umea": {"colour": "#053061", "symbol": "hourglass"},
    "Uppsala": {"colour": "#663399", "symbol": "square"},
    "Vasteras": {"colour": "#b691d2", "symbol": "hourglass"},
}

wastewater_data = pd.read_csv(
    "https://blobserver.dc.scilifelab.se/blob/SLU_wastewater_data.csv",
    sep=",",
)
# wastewater_data = pd.read_csv("ww-data.csv", sep=",")

# We are only intetrested in the covid data
ww_sars = wastewater_data[(wastewater_data["target"] == "SARS CoV-2")]

# Get unique list of city to loop over
all_cities = sorted(ww_sars.city.drop_duplicates().to_list())

# # Compile plot data by looping over the cities
plot_data = {}
for index, method in enumerate(["pmmov_normalised", "copies_l", "copies_day_inhabitant"], 1):
    plot_data[method] = []
    for city in all_cities:
        ww_city_data = ww_sars[(ww_sars["city"] == city)].sort_values(by=["sampling_date"])
        plot_data[method].append(
            go.Scatter(
                name=city,
                x=ww_city_data["sampling_date"],
                y=ww_city_data[method],
                mode="lines+markers",
                marker=dict(color=cities_graph_info[city]["colour"], size=7),
                marker_symbol=cities_graph_info[city]["symbol"],
                line=dict(color=cities_graph_info[city]["colour"], width=2),
                visible=True if index == 1 else False
            )
        )

fig = go.Figure(data=plot_data["pmmov_normalised"])
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=14),
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.99, font=dict(size=14)),
    hovermode="x unified",
    hoverdistance=1,
    margin=dict(l=0, r=0, t=0, b=170),
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
    hoverformat="%b %d, %Y (week %V)",
)
fig.update_yaxes(
    title="<b>SARS-Cov-2/PMMoV x 1000</b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
)
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            pad={"l": 10, "t": 25},
            active=0,
            x=-0.175,
            xanchor="left",
            y=1.125,
            yanchor="top",
            buttons=list(
                [
                    dict(
                        label="Pmmov Normalised Content",
                        method="update",
                        args=[
                            {
                                "name": get_plot_data(plot_data["pmmov_normalised"],"name"),
                                "x": get_plot_data(plot_data["pmmov_normalised"],"x"),
                                "y": get_plot_data(plot_data["pmmov_normalised"],"y"),
                            },
                            {
                                "yaxis.title": dict(text="<b>SARS-CoV2/PMMoV x 1000</b>")
                            }
                        ],
                    ),
                    dict(
                        label="Genome Copies Concentration",
                        method="update",
                        args=[
                            {
                                "name": get_plot_data(plot_data["copies_l"],"name"),
                                "x": get_plot_data(plot_data["copies_l"],"x"),
                                "y": get_plot_data(plot_data["copies_l"],"y"),
                            },
                            {
                                "yaxis.title": dict(text="<b>SARS-CoV2 copies/liter</b>")
                            }
                        ],
                    ),
                    dict(
                        label="Genome Copies/Day/Inhabitant",
                        method="update",
                        args=[
                            {
                                "name": get_plot_data(plot_data["copies_day_inhabitant"],"name"),
                                "x": get_plot_data(plot_data["copies_day_inhabitant"],"x"),
                                "y": get_plot_data(plot_data["copies_day_inhabitant"],"y"),
                            },
                            {
                                "yaxis.title": dict(text="<b>SARS-CoV2 copies/inhabitant/day</b>")
                            }
                        ],
                    ),
                ]
            ),
        ),
        dict(
            type="buttons",
            direction="right",
            pad={"r": 10, "t": 25},
            active=0,
            x=1.1,
            xanchor="right",
            y=1.125,
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

# # Saves as a json file
# fig.write_json("wastewater_combined_slu_regular.json")


print(fig.to_json())
