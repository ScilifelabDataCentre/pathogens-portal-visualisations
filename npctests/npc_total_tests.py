''' 
This script is designed to handle the data processing and visualization for the National Pandemic Centre's test data. It fetches the data directly from a specified URL (Blobserver), processes it for analysis, and generates a comprehensive plot using Plotly. This plot provides insights into the total tests conducted by the National Pandemic Centre.
'''
import pandas as pd
import plotly.express as px
import plotly.io as pio


url = "https://blobserver.dc.scilifelab.se/blob/NPC-statistics-data-set.csv"

# Read data
npc_data = pd.read_csv(url)
total_tests = npc_data['count'].sum()
total_tests = npc_data['count'].sum()

# total count of positive tests in column 'count' based on the column 'class' 
total_positive = npc_data[npc_data['class'] == 'positive']['count'].sum()

# total count of negative tests in column 'count' based on the column 'class'
total_negative = npc_data[npc_data['class'] == 'negative']['count'].sum()

# total count of invalid/inconclusive tests in column 'count' based on the column 'class'
total_inv = npc_data[npc_data['class'] == 'invalid/inconclusive']['count'].sum()


# Create a dictionary with the data for the bar chart
data = {
    'class': ['Positive', 'Negative', 'Invalid/Inconclusive'],
    'Count': [total_positive, total_negative, total_inv]
}

df = pd.DataFrame(data) # Create a DataFrame from the dictionary

# #bar chart using plotly express
plot_npc_total_tests = px.bar(df, y='class', x='Count', text='Count',orientation='h',)

# Customizing the bar chart traces
plot_npc_total_tests.update_traces(textposition='outside',
                  marker_color=["#F47BA4", "#1A6978" ,"#FCC892"], 
                  marker_line_color='black', 
                  marker_line_width=2,
                  hovertemplate="""Class: <b>%{y}</b><br>Count: <b>%{x}</b>""",
                  hoverlabel_bgcolor='white',
                  )

# Customizing layout
plot_npc_total_tests.update_layout(title_text='<b>Total number of tests</b>',
                                        plot_bgcolor="white",
                                        autosize=True,
                                        title_x=0.5,
                                        xaxis_title=None,
                                        yaxis_title=None,
                                        margin=dict(l=0, r=200, t=50, b=0),  # Adjust margins to fit 
                                    )

# Customizing x-axis
plot_npc_total_tests.update_xaxes(
    range=[0, 600000],
    showgrid=True,
    linecolor="black",
    gridcolor="lightgrey",
    zeroline=True,
    zerolinecolor="black",
)

#Customizing y-axis
plot_npc_total_tests.update_yaxes(
    linecolor="black",
    zeroline=True,
    zerolinecolor="black",
)

# # Add total sum annotation
plot_npc_total_tests.add_annotation(
    x=1.02,
    y=0.8,
    xanchor='left',
    xref='paper',
    yref='paper',
    text=f"<b>Sum total</b><br>{total_tests}",
    showarrow=False,
    font_size=14,
    align='center',
    bordercolor="black",
    borderwidth=2,
    borderpad=10,
    bgcolor="white",
)

plot_npc_total_tests.show()

# Save the plot as a json file
pio.write_json(plot_npc_total_tests, 'npc_total_tests.json')