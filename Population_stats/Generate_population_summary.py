import pandas as pd

Raw_scb_data = pd.read_excel(
    # This link is unfortunately not consistent, so will need to change every quarter of the year (Jan, April, July, September)
    "https://www.scb.se/contentassets/cb47e70ddc6b4ed38e67c075b1d59260/tabkv42021eng.xlsx",
    sheet_name="Total",
    header=4,
    engine="openpyxl",
    keep_default_na=False,
)

# note above - header isnt row 0
# drop first 4 rows after header (just blank additional header rows)

Raw_scb_data = Raw_scb_data.drop(range(4))

Raw_scb_data = Raw_scb_data[["Code", "County", "Population"]]

Raw_scb_data = Raw_scb_data.replace(" ", "", regex=True)

# Select by county codes

county_list = [
    "01",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "12",
    "13",
    "14",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
]

Raw_scb_data = Raw_scb_data[Raw_scb_data["Code"].isin(county_list)]

Raw_scb_data = Raw_scb_data.rename(columns={"County": "Lan"})

Raw_scb_data = Raw_scb_data.replace("VästraGötaland", "Västra Götaland", regex=True)

Raw_scb_data = Raw_scb_data[["Lan", "Population"]]

Raw_scb_data.to_excel("SCB_pop_data.xlsx")
