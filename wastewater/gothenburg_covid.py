import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from datetime import date, timedelta
from plotly.io import write_image

wastewater_data = pd.read_excel(
    "https://blobserver.dc.scilifelab.se/blob/wastewater_data_gu_allviruses.xlsx",
    sheet_name="all_viruses",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)
# wastewater_data = pd.read_csv(
#     "https://blobserver.dc.scilifelab.se/blob/wastewater_data_gu.csv",
#     sep=";",
# )

wastewater_data["year"] = (wastewater_data["week"].str[:4]).astype(int)
wastewater_data["week_no"] = wastewater_data["week"].str[-3:]
wastewater_data["week_no"] = (
    wastewater_data["week_no"].str.replace("-", "", regex=True)
).astype(int)
# set the date to the start of the week (Monday)
wastewater_data["day"] = 1
wastewater_data["date"] = wastewater_data.apply(
    lambda row: dt.fromisocalendar(row["year"], row["week_no"], row["day"]), axis=1
)

# colours for plot
colours = px.colors.diverging.RdBu

wastewater_data.rename(columns={"SARS-CoV-2": "covid"}, inplace=True)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name="Relative amount of SARS-CoV-2",
        x=wastewater_data.date,
        y=wastewater_data.covid,
        marker_color=px.colors.diverging.RdBu[1],
        customdata=wastewater_data,
        hovertemplate="Week: %{customdata[0]}<br>Relative amount of SARS-CoV-2: %{y}<extra></extra>",
    )
)

fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    font=dict(size=12),
    margin=dict(r=0, t=0, b=0, l=0),  # changed from 65 when buttons remove
    legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.99, font=dict(size=16)),
    hovermode="x unified",
    hoverdistance=1,
)
fig.update_xaxes(
    title="<br><b>Date (Week Commencing)</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
    # rangebreaks=[dict(values=dd)],
)
fig.update_yaxes(
    title="<b>Number of SARS-CoV-2 viral genome copies per day</b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    tickformat="2e",
    # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
    zeroline=True,
    zerolinecolor="black",
    # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
    rangemode="tozero",
    # Below sets the range to be at least 10 times
    range=[
        0,
        max((wastewater_data["covid"].mean()) * 10, max(wastewater_data.covid)) * 1.05,
    ],
)

# fig.add_vrect(
#     x0="2022-11-10",
#     x1="2023-01-06",
#     # annotation_text="Data missing",
#     # annotation_position="top left",
#     fillcolor=px.colors.diverging.RdBu[10],
#     opacity=0.5,
#     line_width=0,
# )
# fig.add_vline(
#     x=datetime.datetime.strptime("2023-01-11", "%Y-%m-%d").timestamp() * 1000,
#     # annotation_text=" Break in data collection",
#     #    annotation_position="top left",
#     fillcolor=px.colors.diverging.RdBu[10],
#     opacity=1,
#     line_width=5,
#     line_dash="dash",
# )

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
# fig.write_json("wastewater_gothenburg_new.json")

# fig.write_image("wastewater_gothenburg_line.png")

print(fig.to_json())
