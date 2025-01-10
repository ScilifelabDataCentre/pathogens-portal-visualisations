
import argparse
import pandas as pd

from datetime import datetime as dt
from pathlib import Path


def clean_and_calculate_percentages(data_path):
    """
    Reads strain data, calculates weekly percentages for different lineage groups,
    and returns the updated DataFrame.

    Args:
        data_path (str): Path to the CSV file containing strain data.

    Returns:
        pd.DataFrame: Updated DataFrame with calculated columns.
    """

    strain_data = pd.read_csv(data_path, sep=",")

    # Express date, Year-Week
    strain_data["date"] = pd.to_datetime(strain_data["date"])
    strain_data["Year-Week"] = strain_data["date"].dt.strftime("%Y-%W")
    strain_data["Year-Week"] = strain_data["Year-Week"].apply(
        lambda x: x.replace("2023-00", "2022-52")
    )

    # Calculate total entries per week
    strain_data["strains_weekly"] = strain_data.groupby("Year-Week").transform("size")

    # Lineage group calculations
    # strain_data["no_lineage5"] = strain_data.groupby(["Year-Week", "lineage_groups05"]).transform("size")
    # strain_data["percentage_lineage5"] = (
    #     strain_data["no_lineage5"] / strain_data["strains_weekly"]
    # ) * 100
    
    strain_data["no_lineage6"] = strain_data.groupby(["Year-Week", "lineage_groups06"]).transform("size")
    strain_data["percentage_lineage6"] = (
        strain_data["no_lineage6"] / strain_data["strains_weekly"]
    ) * 100

    strain_data["no_lineage4"] = strain_data.groupby(["Year-Week", "lineage_groups04"]).transform("size")
    strain_data["percentage_lineage4"] = (
        strain_data["no_lineage4"] / strain_data["strains_weekly"]
    ) * 100

    strain_data["no_lineage1"] = strain_data.groupby(["Year-Week", "lineage_groups01"]).transform("size")
    strain_data["percentage_lineage1"] = (
        strain_data["no_lineage1"] / strain_data["strains_weekly"]
    ) * 100
    
    # drop column
    # strain_data = strain_data.drop(columns=["EPI_ISL_ID","lineage", "WHO_label", "lineage_full", "no_lineage1", "no_lineage4", "no_lineage5","date", "strains_weekly"])  
    strain_data = strain_data.drop(columns=["EPI_ISL_ID","lineage", "WHO_label", "lineage_full", "no_lineage1", "no_lineage4", "no_lineage6","date", "strains_weekly"])  
    
    # strain_data
    return strain_data

# to run this script from the command line, use the following command: 
# python3 data-cleaning.py file-path.csv
# the output will be saved in the data folder as lineage-cleaned-data.csv
# the cleaned data should be uploaded to the blob server
# then plots will be created by using the cleaned data from the blob server
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean and calculate percentages of strain data.')
    parser.add_argument('data_path', type=str, help='Path to the CSV file containing strain data.')
    parser.add_argument('--output', type=str, help='Path to where the output should be generated. If not specified, created in current directory')
    args = parser.parse_args()

    cleaned_data = clean_and_calculate_percentages(args.data_path)

    # Create output directory is doesn't exist
    output_file = "lineage-cleaned-data.csv"
    if args.output:
        Path(args.output).mkdir(parents=True, exist_ok=True)
        output_file = "%s/%s" % (args.output, output_file) 

    # Save data to CSV
    cleaned_data.to_csv(output_file, index=False)

    print("Data cleaning and CSV generation complete!")