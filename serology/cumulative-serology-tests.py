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


# Set figure traces
fig.update_traces(
    hovertemplate=None,
    marker_color="white",
    marker_line_width=2,
    marker_size=8,
)


# Set figure layout
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    margin=dict(r=180, t=0, b=0, l=0),
    hovermode="x unified",
    legend_traceorder="reversed",
    legend_title="<b>Test results</b>",
)


# Set axis properties (type='category' ensures one bar per week)
fig.update_xaxes(
    type="category",
    title="<b>Date (year-week)</b>",
    range=[0, serology_data["class"].value_counts().max()]
)


fig.update_yaxes(
    title="<b>Cumulative number of tests</b>",
    linecolor="black",
    showgrid=True,
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
    range=[-1000, serology_data["cumulative sum"].max()+10000]
)


# Add an annotation to display the total number of tests and the proportion of positive tests

# Calculate the total sum
sum_total = serology_data["count"].sum()

# Calculate the proportion of positive tests
sum_positive_negative = (
    serology_data[serology_data["class"] == "positive"]["count"].sum()
    + serology_data[serology_data["class"] == "negative"]["count"].sum()
)

proportion_positive = 100 * (
    serology_data[serology_data["class"] == "positive"]["count"].sum()
    / sum_positive_negative
)

# Format accordingly
proportion_positive = f"{proportion_positive:.2f}%"


# Add figure annotation
fig.add_annotation(
    text=f"<b>Sum total</b><br>{sum_total}<br><br><b>Proportion<br>positive</b><br>{proportion_positive}",
    showarrow=False,
    xref="paper",
    yref="paper",
    xanchor="left",
    x=1.02,
    y=0.585,
    bgcolor="#FFFFFF",
    bordercolor="black",
    borderwidth=2,
    borderpad=10,
    font_color="black",
    font_size=14,
)


# Display the graph
# fig.show()


# Save figure to JSON file
pio.write_json(fig, "cumulative_serology_tests.json")
