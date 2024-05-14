''' 
This script reads wastewater data from a 
URL (Blobserver), 
processes it, 
and creates a bar chart using Plotly.
'''
import pandas as pd
import plotly.express as px
import plotly.io as pio
# import kaleido

# Read data from URL
url = "https://blobserver.dc.scilifelab.se/blob/wastewater_data_Stockholm.xlsx"

# The data is read from an Excel file, specifying the engine and the columns to use
wastewater_data = pd.read_excel(url,
                                engine="openpyxl",
                                usecols=["Weeks", "Stockholm weekly Gene copy number/week (raw wastewater) with bovine + PMMoV factor"],)
# Renaming the columns for easier reference
wastewater_data.columns = ["Weeks", "Gene"]

# Remove "Week" and "*" from the "Weeks" column and convert to numeric
# This is done to clean the data and make it easier to work with
wastewater_data["Weeks"] = wastewater_data["Weeks"].str.replace("Week", "").str.replace("*", "").astype(int)

# print(wastewater_data)

#To add missing weeks to the data we need to make sure that the data is sorted by the "Weeks" column first for 2020 and then for 2021
first_series = pd.Series(range(16, 54))

# Create the second Series
second_series = pd.Series(range(1, 35))

# Combine the Series using concatenation
combined_series = pd.concat([first_series, second_series])
combined_series = combined_series.reset_index(drop=True)
all_weeks = pd.DataFrame({'Weeks': combined_series, 'Gene': 0}) # Create a DataFrame with the combined Series for all weeks

# all weeks of 2020 are in the first 30 rows of the data and stored in first
first = wastewater_data.loc[:30]

min_week = first['Weeks'].min()
max_week = first['Weeks'].max()
complete_weeks = range(min_week, max_week + 1)
missing_weeks = [week for week in complete_weeks if week not in first['Weeks'].tolist()]
missing_df = pd.DataFrame({'Weeks': missing_weeks, 'Gene': 0})
first = pd.concat([first, missing_df], ignore_index=True, sort=False)
first = first.sort_values(by='Weeks')

# all weeks of 2021 are from 31st row until end of the data and stored in second
second = wastewater_data.loc[31:]
min_week = second['Weeks'].min()
max_week = second['Weeks'].max()
complete_weeks = range(min_week, max_week + 1)
missing_weeks = [week for week in complete_weeks if week not in second['Weeks'].tolist()]

missing_df = pd.DataFrame({'Weeks': missing_weeks, 'Gene': 0.0})
second = pd.concat([second, missing_df], ignore_index=True, sort=False)
second = second.sort_values(by='Weeks')

final = pd.concat([first, second], ignore_index=True, sort=False)


#updating the wastewater_data with the final data that includes all weeks
wastewater_data = final

#to get an index of the row where the value in the "Weeks" column is equal to 53
# print(final.index[final['Weeks'] == 53].tolist())


# This function formats the week number and year into a string format.
# The year is determined based on the index.
def format_week(week_num, index):
    if index <= 37: # this is the index where the year changes from 2020 to 2021 after week 53
        year = "2020"
    else:
        year = "2021"
    year_week = f"{year}-W{week_num:02d}"
    return year_week

# Applying the format_week function to the "Weeks" column
wastewater_data["Formatted_Weeks"] = [
    format_week(row["Weeks"], index) for index, row in wastewater_data.iterrows()
]

# print(wastewater_data)
#Convert a number in scientific notation to a fixed-point (10^18) representation.
def convert_to_fixed_10_18(scientific_notation):
    # Convert the scientific notation to float, if it's not an empty string, else assign 0
    value = float(scientific_notation) if scientific_notation != '' else 0
    # Convert the float to an integer and divide by 10^18 to get the fixed-point representation
    fixed_value = int(value) / (10 ** 18)
    return fixed_value

# Apply the convert_to_fixed_10_18 function to the 'Gene' column of the dataframe
wastewater_data['fixed_Gene'] = wastewater_data['Gene'].apply(convert_to_fixed_10_18)

# print(wastewater_data)
# Create plotly figure
fig = px.bar(
    wastewater_data,
    x="Formatted_Weeks",
    y="fixed_Gene",
    custom_data=wastewater_data,
    )

# Update the figure traces
fig.update_traces(
    marker_color=px.colors.diverging.RdBu[1],
    hovertemplate="""
    Week: <b>%{x} </b> <br>
    Gene copy number with <b>%{y}</b> bovine + PMMoV factor (× 10^18)
    """,
    )


# Set figure layout
fig.update_layout(
    plot_bgcolor="white",
    autosize=True,
    margin=dict(r=0, t=10, b=0, l=0),
    hovermode='closest',
    hoverdistance=1,
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    ),
    
)

# Update x-axis properties
fig.update_xaxes(
    tickvals=wastewater_data["Formatted_Weeks"], 
    ticktext=wastewater_data["Formatted_Weeks"].str.replace('W',''),
    title_text="Year-Week",
    title_font_weight="bold",
    linecolor="black",
    tickangle=45,
)

# Update y-axis properties
fig.update_yaxes(
    title_text="Gene copy number with bovine + PMMoV factor (× 10^18)",
    title_font_weight="bold",
    showgrid=True,
    linecolor="black",
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)

# Display the chart
# fig.show()

# #write the figure to a json file
# pio.write_json(fig, "wastewater_data_stockholm.json")

# #writing the figure to a .png
# fig.write_image("wastewater_graph_stockholm.png")