import argparse
import os
import pandas as pd

aparser = argparse.ArgumentParser(description="Generate summary file for POSTCOVID")
aparser.add_argument("--output-dir", nargs="?", default="postcovid_plots",
                     help="Output directory where the files will be saved")
args = aparser.parse_args()

## REMEMBER THAT WEEK NUMBER WILL AND POPULATION DATA MIGHT REQUIRE UPDATE
# Import and sort data
postcovid_df = pd.read_excel(
    "https://www.socialstyrelsen.se/globalassets/sharepoint-dokument/dokument-webb/statistik/statistik-postcovid.xlsx",
    sheet_name="Postcovid - län",
    header=6,
    engine="openpyxl",
    keep_default_na=False,
)

postcovid_df = postcovid_df[1:]
postcovid_df = postcovid_df[:-2]
postcovid_df.drop(postcovid_df.columns[[2, 3, 4, 6]], axis=1, inplace=True)
postcovid_df.rename(
    columns={
        "Unnamed: 0": "Lan",
        "Antal": "Antal_kodU099",
        "Antal.1": "Antal_kodU089",
    },
    inplace=True,
)

# print(postcovid_df)

SCB_population = pd.read_excel(
    "https://blobserver.dc.scilifelab.se/blob/SCB_pop_data.xlsx",
    sheet_name=0,
    header=0,
    engine="openpyxl",
    keep_default_na=False,
)

# SCB_population.drop(SCB_population.columns[[0]], axis=1, inplace=True)
# print(SCB_population)

postcov_pop = pd.merge(postcovid_df, SCB_population, how="left", on="Lan")


# postcov_pop.drop(postcov_pop.columns[[3]], axis=1, inplace=True)
postcov_pop["proc_kodU099_pop"] = (
    postcov_pop["Antal_kodU099"] / postcov_pop["Population"]
) * 100
postcov_pop["proc_kodU089_pop"] = (
    postcov_pop["Antal_kodU089"] / postcov_pop["Population"]
) * 100

# print(postcov_pop)

if not os.path.isdir(args.output_dir):
    os.mkdir(args.output_dir)
postcov_pop.to_csv(os.path.join(args.output_dir, "Summary_postcovid_statistics.csv"))

# The following data is not available anymore, so skip running this part
# Should be removed if not alternatives were found
#
# cases_df = pd.read_excel(
#     "https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data",
#     sheet_name="Veckodata Region",
#     header=0,
#     engine="openpyxl",
#     keep_default_na=False,
# )
#
# total_cases = cases_df[
#     (cases_df["år"] == cases_df["år"].iloc[-1])
#     & (cases_df["veckonummer"] == cases_df["veckonummer"].iloc[-1])
# ]  # to select latest weeks data
# keep_cols = ["Region", "Kum_antal_fall"]
# total_cases = total_cases[keep_cols]
#
# total_cases.rename(
#     columns={
#         "Region": "Lan",
#     },
#     inplace=True,
# )
#
# total_cases = total_cases.replace(
#     {"Jämtland Härjedalen": "Jämtland", "Sörmland": "Södermanland"},
# )


# # total_cases.drop(total_cases.columns[0], axis=1, inplace=True)

# postcov_summary = pd.merge(postcov_pop, total_cases, how="left", on="Lan")

# postcov_summary = pd.merge(postcov_pop, total_cases, how="left", on="Lan")
#
# postcov_summary["proc_kodU099_fall"] = (
#     postcov_summary["Antal_kodU099"] / postcov_summary["Kum_antal_fall"]
# ) * 100
# postcov_summary["proc_kodU089_fall"] = (
#     postcov_summary["Antal_kodU089"] / postcov_summary["Kum_antal_fall"]
# ) * 100
# # print(postcov_summary)
#
# if not os.path.isdir(args.output_dir):
#     os.mkdir(args.output_dir)
# postcov_summary.to_csv(os.path.join(args.output_dir, "Summary_postcovid_statistics.csv"))
