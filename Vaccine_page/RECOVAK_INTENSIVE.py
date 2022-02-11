import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime as dt

# Import data

RECO_intense = pd.read_excel(
    "data/reco_intensive_care_vs_vaccine.xlsx",
    sheet_name="Sheet1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# set date

RECO_intense[["Year", "Week"]] = (
    RECO_intense["wk"].str.split("w", expand=True).astype(int)
)

RECO_intense["day"] = 1  # set date as Monday

RECO_intense["date"] = RECO_intense.apply(
    lambda row: dt.fromisocalendar(row["Year"], row["Week"], row["day"]), axis=1
)

# Make stacked bar chart

map_colour = px.colors.diverging.RdBu

fig = go.Figure(
    data=[
        # go.Bar(
        #     name="Three doses",
        #     x=RECO_intense.date,
        #     y=RECO_intense.vacc3,
        #     marker=dict(color=map_colour[10], line=dict(color="#000000", width=1)),
        # ),
        go.Bar(
            name="Two doses",
            x=RECO_intense.date,
            y=RECO_intense.vacc2,
            marker=dict(color=map_colour[7], line=dict(color="#000000", width=1)),
            customdata=(RECO_intense["c19_i1"]),
            hovertemplate="%{y} <b>Tot</b>: %{customdata}",
        ),
        go.Bar(
            name="One dose",
            x=RECO_intense.date,
            y=RECO_intense.vacc1,
            marker=dict(color=map_colour[4], line=dict(color="#000000", width=1)),
        ),
        go.Bar(
            name="Unvaccinated",
            x=RECO_intense.date,
            y=RECO_intense.vacc0,
            marker=dict(color=map_colour[1], line=dict(color="#000000", width=1)),
            # below commented text would put numbers on top of bars. Looks small though when numbers are bigger, doesn't work well, keep in hover.
            # text=RECO_intense["c19_i1"],
            # textposition="outside",
        ),
    ]
)

fig.update_layout(
    barmode="stack",
    plot_bgcolor="white",
    autosize=False,
    font=dict(size=18),
    margin=dict(r=250, t=0, b=0, l=0),
    width=1500,
    height=800,
    legend=dict(
        y=0.95, x=1.0, title="<b>Vaccination status<br></b>", font=dict(size=22)
    ),
    showlegend=True,
    hoverlabel=dict(align="left"),
    hovermode="x unified",
)

# fig.add_vline(
#     x=dt.strptime("2020-12-21", "%Y-%m-%d").timestamp() * 1000,
#     annotation_position="top left",
#     #    annotation=dict(font_size=16),
#     annotation_text="First doses start ",
#     line_width=2,
# )

# fig.add_vline(
#     x=dt.strptime("2021-01-04", "%Y-%m-%d").timestamp() * 1000,
#     annotation_text=" Second doses start",
#     line_width=2,
# )

# fig.add_vline(
#     x=dt.strptime("2020-12-21", "%Y-%m-%d").timestamp() * 1000,
#     annotation_text="Third vaccinations",
# )

# modify x-axis
fig.update_xaxes(
    title="<br><b>Date</b>",
    showgrid=True,
    linecolor="black",
    range=["2020-01-01", max(RECO_intense.date)],
)

highest_y_value = max(
    RECO_intense["c19_i1"],
)

# modify y-axis
fig.update_yaxes(
    title="<b>Admissions to ICU<br></b>",
    showgrid=True,
    gridcolor="lightgrey",
    linecolor="black",
    dtick=50,
    range=[0, int(highest_y_value * 1.1)],
)
# if not os.path.isdir("Plots/"):
#     os.mkdir("Plots/")
# fig.show()
fig.write_image("Plots/draft_plot_vaccine_intensivecare.png")
