'''
This script is designed to handle the data processing and visualization for the National Pandemic Centre's test data. It fetches the data directly from a specified URL (Blobserver), processes it for analysis, and generates a comprehensive plot using Plotly. This plot provides insights into the daily tests conducted by the National Pandemic Centre.
'''
import pandas as pd
import plotly.express as px
import plotly.io as pio


url = "https://datagraphics.dc.scilifelab.se/dataset/bbbaf64a25a1452287a8630503f07418.csv"

# Read data
npc_data = pd.read_csv(url)

plot_npc_tests_daily = px.bar(npc_data, x='date', y='count', color='class',
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
plot_npc_tests_daily.update_traces(
    hovertemplate=None,
)

plot_npc_tests_daily.update_layout(title_text=None,
                                        plot_bgcolor="white",
                                        autosize=True,
                                        xaxis_title="<b>Date</b>",
                                        yaxis_title="<b>Number of tests</b>",
                                        margin=dict(r=0, t=0, b=0, l=0),
                                        hovermode="x unified",
                                        legend_traceorder="reversed",
                                    )
# Customizing x-axis
plot_npc_tests_daily.update_xaxes(
                                linecolor="black",
                                zeroline=True,
                                zerolinecolor="black",
                            )
#Customizing y-axis
plot_npc_tests_daily.update_yaxes(
                            linecolor="black",
                            zeroline=True,
                            gridcolor="lightgrey",
                            zerolinecolor="black",
                        )
plot_npc_tests_daily.show()

# Save the plot as a json file
pio.write_json(plot_npc_tests_daily, 'npc_tests_daily.json')