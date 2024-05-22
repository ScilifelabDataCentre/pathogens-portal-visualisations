import pandas as pd
import plotly.express as px
import plotly.io as pio


# Read CSV file into a DataFrame
serology_data = pd.read_csv(
    "https://blobserver.dc.scilifelab.se/blob/Serology-testing-statistics-dataset-20202021.csv",
    header=0,
)


# Create a stacked bar graph using Plotly Express
fig = px.bar(
    serology_data,
    x="week",
    y="count",
    color="class",
    color_discrete_map={
        "R&D": "#FCC892",
        "positive": "#F47BA4",
        "negative": "#1A6978",
    },
    category_orders={
        "class": [
            "negative",
            "positive",
            "R&D",
        ]
    },
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
    legend_title="<b>Test results</b>",
)


# Set axis properties (type='category' ensures one bar per week)
fig.update_xaxes(
    type="category",
    title="<b>Date (year-week)</b>",
    linecolor="black",
)


fig.update_yaxes(
    title="<b>Number of tests</b>",
    linecolor="black",
    showgrid=True,
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)


# Display the graph
# fig.show()


# Save figure to JSON file
pio.write_json(fig, "weekly_serology_tests.json")
