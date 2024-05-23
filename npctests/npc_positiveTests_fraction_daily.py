'''
This script is designed to handle the data processing and visualization for the National Pandemic Centre's test data. It fetches the data directly from a specified URL (Blobserver), processes it for analysis, and generates a comprehensive plot using Plotly. This plot provides insights into the daily positive tests fractions excluding invalid/inconclusive tests conducted by the National Pandemic Centre.
'''
import pandas as pd
import plotly.express as px
import plotly.io as pio


url = "https://datagraphics.dc.scilifelab.se/dataset/bbbaf64a25a1452287a8630503f07418.csv"

# Read data
npc_data = pd.read_csv(url)

only_positive_data = npc_data[npc_data['class'] == 'positive'].copy()

filtered_data = npc_data[npc_data['class'] != 'invalid/inconclusive'].copy()
only_positive_data['total_tests'] = filtered_data.groupby('date')['count'].transform('sum')

only_positive_data['fraction'] = only_positive_data['count'] / only_positive_data['total_tests']*100

# # Create bar chart
plot_npc_positive_fraction_daily = px.bar(only_positive_data, x='date', y='fraction',)

#Customizing the bar chart traces
plot_npc_positive_fraction_daily.update_traces(
                                                hovertemplate=None,
                                                hoverlabel_bgcolor='white',
                                                marker_color="#F47BA4"
                                            )

# Customizing layout
plot_npc_positive_fraction_daily.update_layout(title_text=None,
                                                plot_bgcolor="white",
                                                autosize=True,
                                                xaxis_title="<b>Date</b>",
                                                yaxis_title='<b>Fraction Positive</b>',
                                                hovermode="x unified",
                                            )
# Customizing x-axis
plot_npc_positive_fraction_daily.update_xaxes(
    # showgrid=True,
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
)
#Customizing y-axis
plot_npc_positive_fraction_daily.update_yaxes(
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
    ticksuffix='%',
    gridcolor="lightgrey",
    
)

plot_npc_positive_fraction_daily.show()

# Save the plot as a json file
pio.write_json(plot_npc_positive_fraction_daily, 'npc_positiveTests_fraction_daily.json')