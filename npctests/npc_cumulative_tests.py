"""
This script is designed to handle the data processing and visualization for the National Pandemic Centre's test data. It fetches the data directly from a specified URL (Blobserver), processes it for analysis, and generates a comprehensive plot using Plotly. This plot provides insights into the cumulative tests conducted by the National Pandemic Centre.
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio


url = (
    "https://blobserver.dc.scilifelab.se/blob/NPC-statistics-data-set.csv"
)

# Read data
npc_data = pd.read_csv(url)

npc_data["date"] = pd.to_datetime(npc_data["date"])
cum_data = npc_data.sort_values(by="date")
cum_data.insert(
    len(cum_data.columns), "cumulative sum", cum_data.groupby("class")["count"].cumsum()
)
# print(cum_data)
cum_data["date"] = cum_data["date"].dt.strftime("%Y-%m-%d")

plot_npc_cumulative_tests = px.line(
    cum_data,
    x="date",
    y="cumulative sum",
    color="class",
    labels={"class": "<b>Test Results</b>"},
    color_discrete_map={
        "invalid/inconclusive": "#FCC892",
        "positive": "#F47BA4",
        "negative": "#1A6978",
    },
    category_orders={
        "class": [
            "positive",
            "negative",
            "invalid/inconclusive",
        ]
    },
    markers=True,
)

plot_npc_cumulative_tests.update_traces(
    hovertemplate=None,
    marker_color="white",
    marker_line_width=2,
    marker_size=8,
)

plot_npc_cumulative_tests.update_layout(
    plot_bgcolor="white",
    autosize=True,
    hovermode="x unified",
    legend_traceorder="reversed",
)

plot_npc_cumulative_tests.update_xaxes(
    type="category",
    title="<b>Date</b>",
    nticks=10,
    zeroline=True,
    tickangle=45,
    range=[0, cum_data["class"].value_counts().max()],
    zerolinecolor="black",
)

plot_npc_cumulative_tests.update_yaxes(
    title="<b>Cumulative number of tests</b>",
    linecolor="black",
    showgrid=True,
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)

plot_npc_cumulative_tests.show()

# Save the plot as a json file
pio.write_json(plot_npc_cumulative_tests, "npc_cumulative_tests.json")
