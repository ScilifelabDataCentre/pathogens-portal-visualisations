'''
This script is designed to handle the data processing and visualization for the National Pandemic Centre's test data. It fetches the data directly from a specified URL (Blobserver), processes it for analysis, and generates a comprehensive plot using Plotly. This plot provides insights into the weekly tests conducted by the National Pandemic Centre.
'''
import pandas as pd
import plotly.express as px
import plotly.io as pio


url = "https://blobserver.dc.scilifelab.se/blob/NPC-statistics-data-set.csv"

# Read data
npc_data = pd.read_csv(url)

# Resample to weekly frequency, summing the counts
weekly_data = npc_data

# Resample to weekly frequency, summing the counts
weekly_data['date']= pd.to_datetime(weekly_data['date'])
weekly_data['week_of_year'] = weekly_data['date'].dt.isocalendar().week
weekly_data['year']=(weekly_data['date']+pd.to_timedelta(6-weekly_data['date'].dt.weekday, unit='d')).dt.year

grouped_data = npc_data.groupby(['week_of_year', 'class'])['count'].sum().reset_index()

plot_npc_tests_weekly = px.bar(grouped_data, x='week_of_year', y='count', color='class',
             labels={'count':'Number of Tests', 'date':'Date', 'class':'<b>Test Results</b>'},
             color_discrete_map={
                    "invalid/inconclusive": "#FCC892",
                    "positive": "#F47BA4",
                    "negative": "#1A6978",
                },
                category_orders={
                    "class": [
                        "positive",
                        "negative",
                        "invalid/inconclusive",
                        
                    ]
                },
             )

# Set figure traces
plot_npc_tests_weekly.update_traces(
    hovertemplate=None,
)

#Updating layout
plot_npc_tests_weekly.update_layout(title_text=None,
                                        plot_bgcolor="white",
                                        autosize=True,
                                        xaxis_title="<b>Week</b>",
                                        yaxis_title="<b>Number of tests</b>",
                                        margin=dict(r=0, t=0, b=0, l=0),
                                        hovermode="x unified",
                                        legend_traceorder="reversed",
                                    )

# Customizing x-axis
plot_npc_tests_weekly.update_xaxes(
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
)

#Customizing y-axis
plot_npc_tests_weekly.update_yaxes(
    linecolor="black",
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)
plot_npc_tests_weekly.show()

# Save the plot as a json file
pio.write_json(plot_npc_tests_weekly, 'npc_tests_weekly.json')
