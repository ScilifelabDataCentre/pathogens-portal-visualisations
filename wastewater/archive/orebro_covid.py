import pandas as pd
import plotly.express as px
import plotly.io as pio


# Read the data file from "https://blobserver.dc.scilifelab.se/blob/wastewater_data_Orebro.xlsx"
# and extract the relevant data
wastewater_data = pd.read_excel(
    "https://blobserver.dc.scilifelab.se/blob/wastewater_data_Orebro.xlsx",
    engine="openpyxl",
    usecols=["Vecka", "Medelvärde per vecka"],
)


# Give the columns proper headers
wastewater_data.columns = ["Week", "SARS-CoV2"]


# Convert 'Week' column to integer and 'SARS-CoV2' column to float
wastewater_data["Week"] = wastewater_data["Week"].astype(int).astype(str)
wastewater_data["SARS-CoV2"] = wastewater_data["SARS-CoV2"].astype(float)


# Group by 'Week' with one 'SARS-CoV2' value per week:
# either the mean of existing values or NaN if no data
wastewater_data = (
    wastewater_data.groupby("Week", sort=False)["SARS-CoV2"]
    .apply(lambda x: x.dropna().mean() if not x.dropna().empty else float("NaN"))
    .reset_index()
)


# There are 53 weeks in 2020, let's add the missing rows with NaN values
new_rows = pd.DataFrame({"Week": [52, 53], "SARS-CoV2": [float("NaN"), float("NaN")]})

wastewater_data = pd.concat(
    [wastewater_data.loc[:7], new_rows, wastewater_data.loc[8:]]
).reset_index(drop=True)


# Function to format the 'Week' column according to the year (51 --> 2020-W51)
# Also add markers regarding some data collection features ('*' and '**')
def format_week(week_num, index):

    if index < 10:
        year = "2020"
    else:
        year = "2021"
    year_week = f"{year}-W{week_num}"

    # Add "*" to weeks with missing data
    if index in [8, 9]:
        year_week += "*"

    # Add "**" to weeks with discrepancy in data collection
    if index in [20, 21]:
        year_week += "**"

    return year_week


# Format the 'Week' column with human readable values (iterrows allows to access the index value)
wastewater_data["Week"] = [
    format_week(row["Week"], index) for index, row in wastewater_data.iterrows()
]


# Create a bar chart using Plotly Express
fig = px.bar(
    wastewater_data,
    x="Week",
    y="SARS-CoV2",
    color_discrete_sequence=["#1A6978"],
)


fig.update_traces(
    hovertemplate="SARS-CoV-2 relative<br>to 2020-11-06: <b>%{y}%</b>",
)


# Set figure layout
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    margin=dict(r=0, t=10, b=0, l=0),
    hovermode="x unified",
    hoverdistance=1,
)


fig.update_xaxes(
    title="<br><b>Date (year-week)</b>",
    linecolor="black",
    tickangle=45,
)


fig.update_yaxes(
    title="<b>SARS-CoV-2 relative to value on Nov 6th 2020 (%)</b>",
    showgrid=True,
    linecolor="black",
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)


# Display the chart
# fig.show()


# Save figure to JSON file
pio.write_json(fig, "wastewater_graph_Orebro.json")
