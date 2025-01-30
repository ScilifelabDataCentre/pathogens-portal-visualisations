"""
Script for plotting an outcome visualisation of phase 2 of the PLP Test project
"""


import pandas as pd
import plotly.express as px
import plotly.io as pio


def load_data(filepath):
    """Load the data from a CSV file."""
    return pd.read_csv(filepath)


def preprocess_data(data):
    """Clean and prepare the data for the Gantt chart."""
    # Convert dates and handle missing values
    data['Start date'] = pd.to_datetime(data['Start date'], errors='coerce')
    data['End date'] = pd.to_datetime(data['End date'], errors='coerce').fillna(data['Start date'])

    # Adjust end date for tasks with the same start and end date so they are displayed
    data.loc[data['Start date'] == data['End date'], 'End date'] += pd.Timedelta(days=1)

    # Handle missing values in Method and Comment
    data['Method'] = data['Method'].fillna('None')
    data['Comment'] = data['Comment'].fillna('None')

    # Ensure 'Lab' and 'Method' are strings
    data['Lab'] = data['Lab'].astype(str)
    data['Method'] = data['Method'].astype(str)

    # Create a unique task identifier combining Lab and Stage
    data['Task'] = 'Lab ' + data['Lab'] + ' - ' + data['Stage']

    # Format dates for hover information
    data['Formatted Start'] = data['Start date'].dt.strftime('%b %d, %Y')
    data['Formatted End'] = data['End date'].dt.strftime('%b %d, %Y')

    return data


def create_gantt_chart(data):
    """Generate and customise the Gantt chart using plotly.express.timeline()."""
    # Define color mappings with color-blind safe palettes
    color_mapping = {
        "1": "#4477AA", "2": "#66CCEE", "3": "#228833",
        "4": "#CCBB44", "5": "#EE6677", "6": "#AA3377"
    }

    hover_colors = {
        "1": "#BBCCEE", "2": "#CCEEFF", "3": "#CCDDAA",
        "4": "#EEEEBB", "5": "#FFCCCC", "6": "#EECCDD"
    }

    # Define hover template
    hover_template = (
        "<b>Start Date:</b> %{customdata[0]}<br>"
        "<b>End Date:</b> %{customdata[1]}<br>"
        "<b>Method:</b> %{customdata[2]}<br>"
        "<b>Comment:</b> %{customdata[3]}<extra></extra>"
    )

    # Map colors explicitly
    data['Color'] = data['Lab'].map(color_mapping)
    data['Hover Color'] = data['Lab'].map(hover_colors)

    # Create Gantt chart using plotly.express
    fig = px.timeline(
        data,
        x_start="Start date",
        x_end="End date",
        y="Task",
        color="Color",
        custom_data=["Formatted Start", "Formatted End", "Method", "Comment", "Hover Color"],
        title="PHASE 2 - Lab Stage Duration Analysis",
        color_discrete_sequence=[color_mapping[str(lab)] for lab in sorted(color_mapping.keys())]
    )

    # Customise hover box and template
    fig.for_each_trace(lambda trace: trace.update(
        hoverlabel=dict(
            bgcolor=trace.customdata[0][4],  # use the hover color from custom data
            font_size=12,
            font_color="black",
        ),
        hovertemplate=hover_template
    ))

    # Customise layout
    fig.update_layout(
        plot_bgcolor="white",
        showlegend=False,
        title_x=0.5,
        title_font_size=16
    )

    # Customise axis properties
    fig.update_xaxes(
        title="<b>Date</b>",
        linecolor="black",
        showgrid=True
    )

    fig.update_yaxes(
        title="<b>Analysis stage for each lab</b>",
        linecolor="black",
        showgrid=True,
        autorange="reversed"
    )

    return fig


def main():
    """Run the full workflow."""
    # Dataset URL
    filepath = "https://blobserver.dc.scilifelab.se/blob/PLP-TEST-aggregated-data-phase-2.csv"

    # Load and preprocess data
    data = preprocess_data(load_data(filepath))

    # Generate the Gantt chart
    fig = create_gantt_chart(data)

    # Output (display graph; save JSON file; print JSON to stdout)
    fig.show()
    pio.write_json(fig, "PLP-TEST-labs-analysis-phase-2.json")
    # print(pio.to_json(fig))


if __name__ == "__main__":
    main()
