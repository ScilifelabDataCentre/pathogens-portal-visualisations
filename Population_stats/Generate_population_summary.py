import pandas as pd

Raw_scb_data = pd.read_excel(
    # This link is unfortunately not consistent, so will need to change every quarter of the year (Jan, April, July, September)
    # New data https://www.scb.se/en/finding-statistics/statistics-by-subject-area/population/population-composition/population-statistics/
    "https://www.scb.se/contentassets/63f577487f7f476d8a46c70989696017/be0101_tabkv12024.xlsx",
    sheet_name="Totalt",
    header=7,
    engine="openpyxl",
    keep_default_na=False,
)

# note above - header isnt row 0
# drop first 4 rows after header (just blank additional header rows)

Raw_scb_data = Raw_scb_data.iloc[:, :3]
# Raw_scb_data = Raw_scb_data.iloc[-4:, :]

Raw_scb_data.columns = ["Code", "County", "Population"]

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

Raw_scb_data["Lan"] = Raw_scb_data["Lan"].str.replace("VästraGötaland", "Västra Götaland")

Raw_scb_data = Raw_scb_data[["Lan", "Population"]]

Raw_scb_data.to_excel("SCB_pop_data.xlsx")
