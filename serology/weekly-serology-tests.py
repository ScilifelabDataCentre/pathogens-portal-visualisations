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
    # color_discrete_map={
    #     "R&D": "#FCC892",
    #     "positive": "#F47BA4",
    #     "negative": "#1A6978",
    # },
    # color_discrete_map={
    #     "R&D": "#C480B3",
    #     "positive": "#FAAD5F",
    #     "negative": "#6A754D",
    # },
    # color_discrete_map={
    #     "R&D": "#7DAE9B",
    #     "positive": "#EC9747",
    #     "negative": "#865B77",
    # },
    # color_discrete_map={
    #     "R&D": "#B0AA5B",
    #     "positive": "#AA5BB0",
    #     "negative": "#5BB0AA",
    # },
    # color_discrete_map={
    #     "R&D": "#AAA656",
    #     "positive": "#915497",
    #     "negative": "#60B6B0",
    # },
    color_discrete_map={
        "R&D": "#AAA656",
        "positive": "#60B6B0",
        "negative": "#915497",
    },
    category_orders={
        "class": [
            "positive",
            "negative",
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
)


# Set axis properties (type='category' ensures one bar per week)
fig.update_xaxes(
    type="category",
    title="<b>Week</b>",
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
fig.show()


# Save figure to JSON file
pio.write_json(fig, "../../weekly_serology_tests.json")
