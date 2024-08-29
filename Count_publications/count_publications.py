"""this code generates an interactive graph showing both the
cumulative number of publications in the covid publications datebase
as well as the number added each month. It reads the.json directly from
the database"""
import pandas as pd
import plotly.graph_objects as go
import requests

# get data
res = requests.get("https://publications-covid19.scilifelab.se/publications.json")
txt = res.json()
df = pd.json_normalize(txt["publications"])
df = df[["type", "published"]]

# for now, assume dates with day as 00 are 1st day
df.replace("-00", "-01", regex=True, inplace=True)

# make the cumulative sum of papers published
df.published = pd.to_datetime(df["published"], format="%Y-%m-%d").dt.date
currdate = pd.to_datetime("today").date()
df = df[df["published"] < currdate]
df.sort_values(by="published", inplace=True)
df1 = df["published"].value_counts().sort_index().reset_index()
df1["cumulativecount"] = df1["count"].cumsum()

# find number of papers published in each month
df["year"] = pd.DatetimeIndex(df["published"]).year
df["month"] = pd.DatetimeIndex(df["published"]).month
df["index"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
df2 = df.groupby(["index"]).size().reset_index(name="Number Added")

# make the graph
# bar chart
trace2 = go.Bar(
    x=df2["index"],
    y=df2["Number Added"],
    name="New publications each month",
    marker_color="rgb(222,44,108)",
    hovertemplate="Month: %{x|%B %Y}" + "<br>New publications: %{y}<extra></extra>",
)

# line graph
trace1 = go.Scatter(
    mode="lines",
    x=df1["published"],
    y=df1["cumulativecount"],
    name="Cumulative Total",
    marker_color="rgb(46,104,165)",
    line_width=5,
    hovertemplate="Date: %{x}" + "<br>Total Publications: %{y}<extra></extra>",
)

# combine traces
data = [trace2, trace1]

# figure layout
fig = go.Figure(data=data)
fig.update_layout(
    plot_bgcolor="white",
    font=dict(size=12),
    margin=dict(r=0, t=50),
    autosize=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="left",
        x=-0.1,
    ),
    # width = 1000,
    # height = 500
)
# modify x-axis
fig.update_xaxes(
    title="<b>Date</b>",
    showgrid=True,
    linecolor="black",
    tickangle=45,
    # dtick="M1",
    # set start point of x-axis
    tick0="2020-01-01",
)
# modify y-axis
fig.update_yaxes(
    title="<b>Number of Publications</b>",
    showgrid=True,
    gridcolor="grey",
    linecolor="black",
    # change range to envelope the appropriate range
    range=[0, max(df1["cumulativecount"] + 50)],
)

# Below produces a .html file
# fig.write_html('Count_by_today.html', include_plotlyjs=False, full_html=False)

# Below for testing
# fig.show()
# fig.write_json("COVID_publication_count.json")

# Below for dynamic use
print(fig.to_json())
