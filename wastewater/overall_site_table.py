import pandas as pd
import json
import plotly.graph_objects as go
import os
import numpy as np

# import argparse

# aparser = argparse.ArgumentParser(description="Generate accompanying diagnosis blob")
# aparser.add_argument("--output-dir", nargs="?", default="postcovid_plots",
#                      help="Output directory where the files will be saved")
# args = aparser.parse_args()

# Import and sort data
site_table = pd.read_excel(
    "https://blobserver.dc.scilifelab.se/blob/overall_ww_collection_sites.xlsx",
    # "data/overall_collection_sites.xlsx",
    sheet_name="Sheet 1",
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# site_table = site_table.iloc[
#     0:20,
# ]

site_table.columns = [
    "Area",
    "WWTP",
    "People",
    "Active",
    "Viruses",
    "Group",
]

site_table.sort_values("Area", inplace=True)

# convert weeks to dates
site_table = site_table.replace(r"^\s*$", np.nan, regex=True)


# def add_day(wkyr):
#     return pd.to_datetime((wkyr + "-1"), format="%Y-%W-%w", errors="coerce").dt.date


# site_table[["start_date", "end_date"]] = site_table[["Start", "End"]].apply(add_day)
# # # # Need to setup conversions to Swedish in time!.

fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[5, 7, 5, 5, 5, 5, 5],
            header=dict(
                values=[
                    "<b>Town/City</b>",
                    "<b>WWTP</b>",
                    "<b>Number of people</b>",
                    "<b>Active?</b>",
                    "<b>Viruses monitored</b>",
                    "<b>Group monitoring</b>",
                ],
                align=["left"],
                fill_color="#ededed",
                font=dict(color="black", size=12),
                height=30,
                line=dict(color="#e0e0e0", width=0.05),
            ),
            cells=dict(
                values=(
                    site_table["Area"],
                    site_table["WWTP"],
                    site_table["People"],
                    site_table["Active"],
                    site_table["Viruses"],
                    site_table["Group"],
                ),
                align=["left"],
                fill_color=["white"],
                font=dict(color="black", size=12),
                height=30,
                line=dict(color="#e0e0e0", width=0.05),
            ),
        )
    ]
)
fig.update_layout(margin={"r": 5, "t": 5, "l": 0, "b": 0})
# fig.show()


# # if not os.path.isdir(args.output_dir):
# #     os.mkdir(args.output_dir)
# #fig.write_json(os.path.join(args.output_dir, "slu_site_table.json"))

# Prints as a json file
fig.write_json("wastewater_overallsites.json")

# Below can produce a static image
# fig.write_image("wastewater_overallsites.png")
