# Produces the table associated with the map (improvement on accessibility and add links)
# table will be produced in html, this will produce the input json
import pandas as pd
import json
import numpy as np

# add data
df = pd.read_csv(
    "test_map_points.csv",
    sep=";",
    header=0,
)

# classify levels of wastewater

df["rank"] = np.nan
df["rank"] = (
    df["rank"]
    .mask(df.value == 1, "Low")
    .mask(df.value == 2, "Medium")
    .mask(df.value == 3, "High")
)

# want to drop what we're not using in the table

df = df[["name", "population", "rank", "Link"]]

# Think this will be sufficient to create the required json file for input into a table on portal

js = df.to_json(orient="records")

print(js)
