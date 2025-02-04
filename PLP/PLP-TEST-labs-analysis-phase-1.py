"""
Script for plotting an outcome visualisation of phase 1 of the PLP Test project
"""

import pandas as pd
import plotly.express as px
import plotly.io as pio


def load_data(filepath):
    """Load the data from a CSV file."""
    return pd.read_csv(filepath)


def preprocess_data(data):
    """Clean and prepare the data for visualisation."""
    # Convert Date column to datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    # Remove rows with missing dates
    data = data.dropna(subset=['Date'])

    # Group by Lab and Date to count stages, then merge with original data
    stage_counts = data.groupby(['Lab', 'Date']).size().reset_index(name='Stage_Count')
    data = data.merge(stage_counts, on=['Lab', 'Date'])

    # Ensure Lab is a string for consistent mapping
    data['Lab'] = data['Lab'].astype(str)

    return data


def create_scatter_plot(data):
    """Create and customise the scatter plot."""
    # Define color mappings with color-blind safe palettes
    marker_colors = {
        "1": "#4477AA", "2": "#66CCEE", "3": "#228833",
        "4": "#CCBB44", "5": "#EE6677", "6": "#AA3377"
    }

    hover_colors = {
        "1": "#BBCCEE", "2": "#CCEEFF", "3": "#CCDDAA",
        "4": "#EEEEBB", "5": "#FFCCCC", "6": "#EECCDD"
    }

    # Define hover template
    hover_template = (
        "<b>Date:</b> %{x}<br>"
        "<b>Number of Stages:</b> %{marker.size}<br>"
        "<b>Method:</b> %{customdata[0]}<br>"
        "<b>Comment:</b> %{customdata[1]}<br>"
        "<extra></extra>"
    )

    # Create scatter plot with custom hover details
    fig = px.scatter(
        data,
        x='Date',
        y='Lab',
        color='Lab',
        size='Stage_Count',
        title='PHASE 1 - Lab Activity Timeline <br><sup>marker size corresponds to number of stages</sup>',
        labels={'Date': 'Date', 'Lab': 'Lab ID'},
        color_discrete_map=marker_colors,
        custom_data=['Method', 'Comment'],
    )

    # Apply hover box customisation and marker adjustments
    fig.for_each_trace(lambda trace: trace.update(
        marker=dict(line=dict(width=2, color="white")),
        hoverlabel=dict(
            bgcolor=hover_colors.get(trace.name, "rgba(255,255,255,0.8)"),
            font_size=12,
            font_color="black",
        ),
        hovertemplate=hover_template
    )
                       )

    # Customise plot layout
    fig.update_layout(plot_bgcolor="white", showlegend=False, title_x=0.5)
    fig.update_xaxes(title="<b>Date</b>", linecolor="black")
    fig.update_yaxes(title="<b>Lab ID</b>", linecolor="black", showgrid=True, gridcolor="#DDDDDD")

    return fig


def main():
    """Run the full workflow."""
    # Dataset URL
    filepath = "https://blobserver.dc.scilifelab.se/blob/PLP-TEST-aggregated-data-phase-1.csv"

    # Load and preprocess data
    data = preprocess_data(load_data(filepath))

    # Generate the scatter plot
    fig = create_scatter_plot(data)

    # Output (display graph; save JSON file; print JSON to stdout)
    fig.show()
    pio.write_json(fig, "PLP-TEST-labs-analysis-phase-1.json")
    # print(pio.to_json(fig))


# Run the main function
if __name__ == "__main__":
    main()
