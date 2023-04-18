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
# get just malmö data
sjölunda_wwtp = wastewater_data[(wastewater_data["wwtp"] == "Sjölunda WWTP, Malmö")]
sjölunda_wwtp["year"] = (sjölunda_wwtp["week"].str[:4]).astype(int)
sjölunda_wwtp["week_no"] = sjölunda_wwtp["week"].str[-3:]
sjölunda_wwtp["week_no"] = sjölunda_wwtp["week_no"].str.replace("*", "", regex=True)
sjölunda_wwtp["week_no"] = (
    sjölunda_wwtp["week_no"].str.replace("-", "", regex=True)
).astype(int)
# set the date to the start of the week (Monday)
sjölunda_wwtp["day"] = 1
sjölunda_wwtp["date"] = sjölunda_wwtp.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)
# Limit date range,
max_date = max(sjölunda_wwtp["date"]) + pd.Timedelta(3, unit="d")
min_date = max_date + pd.Timedelta(-17, unit="w")
sjölunda_wwtp_res = sjölunda_wwtp[
    (sjölunda_wwtp["date"] >= min_date) & (sjölunda_wwtp["date"] <= max_date)
]  # added this so that it starts with

# colours for plot
colours = px.colors.diverging.RdBu

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name="Sjölunda",
        x=sjölunda_wwtp.date,
        y=sjölunda_wwtp.value,
        marker_color=px.colors.diverging.RdBu[1],
        # customdata=wastewater_data,
        # hovertemplate="Date (week commencing): %{x}<br>N3-gene copy number per PMMoV<br>gene copy number x 10<sup>4</sup>: %{y}<extra></extra>",
        # hovertemplate="Date (week commencing): %{x}<br>N3-gene copy number per PMMoV<br>gene copy number x 10<sup>4</sup>: %{y}<extra></extra>",
    )
)

fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=14),
    margin=dict(r=150, t=0, b=0, l=0),  # changed from 65 when buttons remove
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.99, font=dict(size=16)),
    hovermode="x unified",
    hoverdistance=1,
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
    range=[min_date, (max_date)],
)
fig.update_yaxes(
    title="<b>N3-gene copy number per<br>PMMoV gene copy number x 10<sup>4</sup></b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
    # zeroline=True,
    # zerolinecolor="black",
    # Below will set the y-axis range to constant, if you wish
    # range=[0, max(wastewater_data["relative_copy_number"] * 1.15)],
)

# fig.update_layout(
#     updatemenus=[
#         dict(
#             type="buttons",
#             direction="right",
#             active=0,
#             x=1.1,
#             y=1.1,
#             xanchor="right",
#             yanchor="top",
#             buttons=list(
#                 [
#                     dict(
#                         label="Reselect all areas",
#                         method="update",
#                         args=[
#                             {"visible": [True]},
#                         ],
#                     ),
#                     dict(
#                         label="Deselect all areas",
#                         method="update",
#                         args=[
#                             {"visible": "legendonly"},
#                         ],
#                     ),
#                 ]
#             ),
#         )
#     ]
# )
# Below can show figure locally in tests
# fig.show()

# Prints as a json file
fig.write_json("wastewater_kthmalmö.json")

# print(fig.to_json())
