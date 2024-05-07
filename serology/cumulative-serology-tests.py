import pandas as pd
import plotly.express as px
import plotly.io as pio


# Read CSV file into a DataFrame
serology_data = pd.read_csv(
    "https://blobserver.dc.scilifelab.se/blob/Serology-testing-statistics-dataset-20202021.csv",
    header=0,
)


# Calculate the cumulative count for each class
serology_data.insert(
    len(serology_data.columns),
    "cumulative sum",
    serology_data.groupby("class")["count"].cumsum(),
)


# Create a line graph using Plotly Express
fig = px.line(
    serology_data,
    x="week",
    y="cumulative sum",
    color="class",
    color_discrete_map={
        "R&D": "#FCC892",
        "positive": "#F47BA4",
        "negative": "#1A6978",
    },
    markers=True,
)


# Set the colours for each class
fig.update_traces(
    marker_color="white",
    marker_line_width=3,
    marker_size=8,
)


# Set figure traces
fig.update_traces(
    hovertemplate=None,
)


# Set figure layout
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    margin=dict(r=0, t=0, b=0, l=0),
    hovermode="x unified",
    legend_traceorder="reversed",
)


# Set axis properties (type='category' ensures one bar per week)
fig.update_xaxes(
    type="category",
    title="<b>Week</b>",
    range=[0, serology_data["class"].value_counts().max()],
)


fig.update_yaxes(
    title="<b>Cumulative number of tests</b>",
    linecolor="black",
    showgrid=True,
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)


# Display the graph
# fig.show()


# Save figure to JSON file
pio.write_json(fig, "cumulative_serology_tests.json")
