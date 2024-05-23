'''
This script is designed to handle the data processing and visualization for the National Pandemic Centre's test data. It fetches the data directly from a specified URL (Blobserver), processes it for analysis, and generates a comprehensive plot using Plotly. This plot provides insights into the weekly positive tests fractions excluding invalid/inconclusive tests conducted by the National Pandemic Centre.
'''
import pandas as pd
import plotly.express as px
import plotly.io as pio


url = "https://datagraphics.dc.scilifelab.se/dataset/bbbaf64a25a1452287a8630503f07418.csv"

# Read data
npc_data = pd.read_csv(url)

npc_data['date']= pd.to_datetime(npc_data['date'])
npc_data['week_of_year'] = npc_data['date'].dt.isocalendar().week
npc_data['year']=(npc_data['date']+pd.to_timedelta(6-npc_data['date'].dt.weekday, unit='d')).dt.year

only_positive_data = npc_data[npc_data['class'] == 'positive'].copy()

filtered_data = npc_data[npc_data['class'] != 'invalid/inconclusive'].copy()
only_positive_data['total_tests'] = filtered_data.groupby('date')['count'].transform('sum')

only_positive_data['fraction'] = only_positive_data['count'] / only_positive_data['total_tests']*100

grouped_data = only_positive_data.groupby(['week_of_year']).agg({'count':'sum', 'total_tests':'sum'}).reset_index()

grouped_data['fraction'] = grouped_data['count'] / grouped_data['total_tests']
grouped_data['percentage'] = grouped_data['fraction']*100
# print(grouped_data)


# Create bar chart
plot_npc_positive_fraction_weekly = px.bar(grouped_data, x='week_of_year', y='fraction')

#Customizing the bar chart traces
plot_npc_positive_fraction_weekly.update_traces(
                        hovertemplate=None,
                        hoverlabel_bgcolor='white',
                        marker_color="#F47BA4"
                        )

# Customizing layout
plot_npc_positive_fraction_weekly.update_layout(title_text=None,
                                   plot_bgcolor="white",
                                    autosize=True,
                                    xaxis_title="<b>Week</b>",
                                    yaxis_title='<b>Fraction Positive</b>',
                                    hovermode='x unified',  
                                    )
# Customizing x-axis
plot_npc_positive_fraction_weekly.update_xaxes(
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
)
#Customizing y-axis
plot_npc_positive_fraction_weekly.update_yaxes(
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
    tickformat='0%',
    # showgrid=True,
    gridcolor="lightgrey",
    
    
)
plot_npc_positive_fraction_weekly.show()


# # Save the plot as a json file
pio.write_json(plot_npc_positive_fraction_weekly, 'npc_positiveTests_fraction_weekly.json')