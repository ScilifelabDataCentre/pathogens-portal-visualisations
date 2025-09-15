
import argparse
import pandas as pd
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
    
    print(f"Data shape: {strain_data.shape}")
    print(f"Columns: {strain_data.columns.tolist()}")
    print("\nFirst few rows:")
    print(strain_data.head())
    
    # Check if required columns exist
    required_columns = ['date', 'lineage_groups01', 'lineage_groups04', 'lineage_groups06']
    missing_columns = [col for col in required_columns if col not in strain_data.columns]
    
    if missing_columns:
        print(f"Warning: Missing required columns: {missing_columns}")
        print("Available columns:", strain_data.columns.tolist())
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Express date, Year-Week - FIXED VERSION
    strain_data["date"] = pd.to_datetime(strain_data["date"])
    
    # Use ISO week format (%V) which follows ISO 8601 standard
    # %V: ISO 8601 week as a zero-padded decimal number (01-53)
    # %W: Week number of the year (00-53)
    # %U: Week number of the year (00-53)
    # strain_data["Year-Week"] = strain_data["date"].dt.strftime("%Y-%W")
    strain_data["Year-Week"] = strain_data["date"].dt.strftime("%Y-%V")
    
    print(f"\nYear-Week range: {strain_data['Year-Week'].min()} to {strain_data['Year-Week'].max()}")
    print(f"Unique Year-Weeks: {strain_data['Year-Week'].nunique()}")

    # Calculate total entries per week
    strain_data["strains_weekly"] = strain_data.groupby("Year-Week").transform("size")
    
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
    
    print(f"\nFinal data shape: {strain_data.shape}")
    print(f"Final columns: {strain_data.columns.tolist()}")
    
    # strain_data
    return strain_data

# to run this script from the command line, use the following command: 
# python3 lineage-data-cleaning.py file-path.csv
# the output will be saved in the data folder as lineage-cleaned-data.csv
# the cleaned data should be uploaded to the blob server
# then plots will be created by using the cleaned data from the blob server
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean and calculate percentages of strain data.')
    parser.add_argument('data_path', type=str, help='Path to the CSV file containing strain data.')
    parser.add_argument('--output', type=str, help='Path to where the output should be generated. If not specified, created in current directory')
    args = parser.parse_args()

    try:
        cleaned_data = clean_and_calculate_percentages(args.data_path)

        # Create output directory is doesn't exist
        output_file = "lineage-cleaned-data.csv"
        if args.output:
            Path(args.output).mkdir(parents=True, exist_ok=True)
            output_file = "%s/%s" % (args.output, output_file) 

        # Save data to CSV
        cleaned_data.to_csv(output_file, index=False)

        print("\nData cleaning and CSV generation complete!")
        print(f"Output saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during data processing: {e}")
        import traceback
        traceback.print_exc()