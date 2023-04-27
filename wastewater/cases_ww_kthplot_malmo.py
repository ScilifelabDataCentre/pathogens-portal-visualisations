import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
from plotly.subplots import make_subplots

from plotly.io import write_image


wastewater_data = pd.read_excel(
    "data/KTH_case_data.xlsx",
    sheet_name="Malmö",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# Change date format
wastewater_data["Week"] = (
    wastewater_data["Week"].str.replace("v", "", regex=True).astype(int)
)
# set the date to the start of the week (Monday)
wastewater_data["day"] = 1
wastewater_data["date"] = wastewater_data.apply(
    lambda row: dt.fromisocalendar(row["Year"], row["Week"], row["day"]), axis=1
)
# # Limit date range,
# max_date = max(sjölunda_wwtp["date"]) + pd.Timedelta(3, unit="d")
# min_date = max_date + pd.Timedelta(-17, unit="w")
# sjölunda_wwtp = sjölunda_wwtp[
#     (sjölunda_wwtp["date"] >= min_date) & (sjölunda_wwtp["date"] <= max_date)
# ]


# colours for plot
colours = px.colors.diverging.RdBu

fig = make_subplots(specs=[[{"secondary_y": True}]])

# # Trace related to wastewater copy number
fig.add_trace(
    go.Bar(
        name="Malmö",
        x=wastewater_data.date,
        y=wastewater_data.N3_mean,
        marker_color=px.colors.diverging.RdBu[1],
        marker_line=dict(width=2, color="black"),
        # customdata=wastewater_data,
        # hovertemplate="Date (week commencing): %{x}<br>N3-gene copy number per PMMoV<br>gene copy number x 10<sup>4</sup>: %{y}<extra></extra>",
    ),
    secondary_y=False,
)

# Traces related to case numbers
fig.add_trace(
    go.Scatter(
        name="COVID-19 cases in Malmö",
        x=wastewater_data.date,
        y=wastewater_data.case_malmö,
        mode="lines+markers",
        marker=dict(color=px.colors.diverging.RdBu[8], size=7),
        marker_symbol="square",
        line=dict(color=px.colors.diverging.RdBu[8], width=2),
    ),
    secondary_y=True,
)
fig.add_trace(
    go.Scatter(
        name="Estimated COVID-19 cases in Malmö",
        x=wastewater_data.date,
        y=wastewater_data.est_case_malmö,
        mode="lines+markers",
        marker=dict(color=px.colors.diverging.RdBu[9], size=7),
        marker_symbol="square",
        line=dict(color=px.colors.diverging.RdBu[9], width=2),
    ),
    secondary_y=True,
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
    #    range=[min_date, (max_date)],
)
# Set up two y-axes (one for cases, one for N3 gene content in wastewater)
fig.update_yaxes(
    title="<b>Total N-gene copy number<br>normalised to PMMoV/week</b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    side="left",
    secondary_y=False,
)
fig.update_yaxes(
    title=dict(text="COVID-19 cases"),
    side="right",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    secondary_y=True,
    # tickmode="sync", #change this to sync axis or not
    rangemode="tozero",
)

## Need to keep the below in case the team decide to add in the functionality before the graph is finalised

# fig.update_layout(
#     # legend=dict(orientation="h"),
#     yaxis=dict(
#         title="<b>N3-gene copy number per<br>PMMoV gene copy number x 10<sup>4</sup></b>",
#         showgrid=True,
#         gridcolor="lightgrey",
#         linecolor="black",
#         side="left",
#         # range=[0, 250],
#     ),
#     yaxis2=dict(
#         title=dict(text="COVID-19 cases"),
#         side="right",
#         showgrid=True,
#         gridcolor="lightgrey",
#         linecolor="black",
#         #        range=[0, 2000],
#         # overlaying="y",
#         # tickmode="sync",
#     ),
# )


# fig.update_yaxes(

#     # below ensures a zeroline on Y axis. Made it black to be clear it's different from other lines
#     # zeroline=True,
#     # zerolinecolor="black",
#     # Below will set the y-axis range to constant, if you wish
#     # range=[0, max(wastewater_data["relative_copy_number"] * 1.15)],
# )

# # fig.update_layout(
# #     updatemenus=[
# #         dict(
# #             type="buttons",
# #             direction="right",
# #             active=0,
# #             x=1.1,
# #             y=1.1,
# #             xanchor="right",
# #             yanchor="top",
# #             buttons=list(
# #                 [
# #                     dict(
# #                         label="Reselect all areas",
# #                         method="update",
# #                         args=[
# #                             {"visible": [True]},
# #                         ],
# #                     ),
# #                     dict(
# #                         label="Deselect all areas",
# #                         method="update",
# #                         args=[
# #                             {"visible": "legendonly"},
# #                         ],
# #                     ),
# #                 ]
# #             ),
# #         )
# #     ]
# # )
# # Below can show figure locally in tests
# fig.show()

# # Prints as a json file
fig.write_json("kth_normalised_COV_malmö.json")

# # print(fig.to_json())
