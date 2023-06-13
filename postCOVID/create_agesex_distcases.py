import argparse
import pandas as pd
import json
import plotly.graph_objects as go
import os

aparser = argparse.ArgumentParser(description="Generate age and sex distribution blob")
aparser.add_argument("--output-dir", nargs="?", default="postcovid_plots",
                     help="Output directory where the files will be saved")
args = aparser.parse_args()

# Import and sort data
age_sex_summ = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - ålder kön",
    header=10,
    engine="openpyxl",
    keep_default_na=False,
)

# trim rows/columns for the two diagnoses
U099 = age_sex_summ.iloc[0:3, 0:7]
U089 = age_sex_summ.iloc[12:15, 0:7]

# organise data for plots

U099 = U099[["Unnamed: 3", "Unnamed: 5", "Unnamed: 1"]]
U089 = U089[["Unnamed: 3", "Unnamed: 5", "Unnamed: 1"]]

U099.columns = ["male", "female", "all"]
U089.columns = ["male", "female", "all"]

U099["age_group"] = ["0-17", "18-69", "70"]
U089["age_group"] = ["0-17", "18-69", "70"]

# plot function for the two plots


def stack_plot(input, name):
    diagnosis = input
    # Make stacked bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="Male",
                x=diagnosis.age_group,
                y=diagnosis.male,
                marker=dict(color="rgb(5,48,97)", line=dict(color="#000000", width=1)),
                hovertemplate="<b>Sex:</b> Male"
                + "<br><b>Age Group:</b> %{x}"
                + "<br><b>Number Diagnosed:</b> %{y}<extra></extra>",
            ),
            go.Bar(
                name="Female",
                x=diagnosis.age_group,
                y=diagnosis.female,
                marker=dict(
                    color="rgb(178,24,43)", line=dict(color="#000000", width=1)
                ),
                hovertemplate="<b>Sex:</b> Female"
                + "<br><b>Age Group:</b> %{x}"
                + "<br><b>Number Diagnosed:</b> %{y}<extra></extra>",
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        autosize=True,
        font=dict(size=14),
        margin=dict(r=110, t=0, b=0, l=0),
        # width=2000, #do not add these parameters for Hugo
        # height=1200,
        showlegend=True,
        legend=dict(
            title="<b>Patient sex</b>",
        ),
    )
    # modify x-axis
    fig.update_xaxes(
        title="<b>Age group</b>",
        showgrid=True,
        linecolor="black",
    )

    highest_y_value = max(
        diagnosis["all"],
    )

    if highest_y_value < 100:
        yaxis_tick = 10
    if highest_y_value > 100:
        yaxis_tick = 10
    if highest_y_value > 1000:
        yaxis_tick = 1000
    if highest_y_value > 10000:
        yaxis_tick = 2000
    if highest_y_value > 20000:
        yaxis_tick = 4000
    if highest_y_value > 30000:
        yaxis_tick = 5000

    # modify y-axis
    fig.update_yaxes(
        title="<b>Number of patients diagnosed<br></b>",
        showgrid=True,
        gridcolor="lightgrey",
        linecolor="black",
        dtick=yaxis_tick,
        range=[0, int(highest_y_value * 1.15)],
    )
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    # fig.show()
    fig.write_json(os.path.join(args.output_dir, "{}_agesex_casedist.json".format(name)))


# make plots by applying function

stack_plot(U099, "U099")
stack_plot(U089, "U089")

# OLD GRAPHICS PLACE:
# you should upload this to https://datagraphics.dc.scilifelab.se/dataset/6b24d7130bef4bf78f567d9c9ad96f59
# need to add to new blob!
