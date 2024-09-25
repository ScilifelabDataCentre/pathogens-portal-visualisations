import pandas as pd
from datetime import datetime as dt


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
    strain_data["no_lineage5"] = strain_data.groupby(["Year-Week", "lineage_groups05"]).transform("size")
    strain_data["percentage_lineage5"] = (
        strain_data["no_lineage5"] / strain_data["strains_weekly"]
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
    strain_data = strain_data.drop(columns=["EPI_ISL_ID","lineage", "WHO_label", "lineage_full", "no_lineage1", "no_lineage4", "no_lineage5","date", "strains_weekly"])  
    # strain_data
    return strain_data


if __name__ == "__main__":
    data_path = "data/Uppsala_data_2024-08-29_Nextclade.csv"  # Replace with your data path
    cleaned_data = clean_and_calculate_percentages(data_path)

    # Save data to CSV
    cleaned_data.to_csv("data/lineage-cleaned-data.csv", index=False)

    print("Data cleaning and CSV generation complete!")