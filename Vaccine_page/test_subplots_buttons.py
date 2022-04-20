import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Bar(x=[1, 2, 3, 4], y=[7, 4, 5, 6], name="bar", visible=True), 1, 1)
fig.add_trace(
    go.Scatter(
        x=[1, 2, 3, 4], y=[4, 2, 5, 3], name="scatt1", visible=False, line_color="red"
    ),
    1,
    2,
)
fig.add_trace(
    go.Scatter(
        x=[1, 2, 3, 4],
        y=[1, 5, 3.5, 6],
        name="scatt2",
        visible=False,
        line_color="green",
    ),
    1,
    2,
)

button1 = dict(
    method="update", args=[{"visible": [True, False, False]}], label="cell 0"
)
button2 = dict(
    method="update", args=[{"visible": [False, True, True]}], label="cell 1 "
)
button3 = dict(
    method="update",
    args=[{"visible": [False, True, False]}],
    label="cell 1 - 1st trace ",
)

button4 = dict(
    method="update", args=[{"visible": [False, False, True]}], label="cell 1-2nd trace "
)
fig.update_layout(
    width=800,
    height=400,
    updatemenus=[
        dict(
            type="buttons",
            buttons=[button1, button2, button3, button4],
            x=1.05,
            xanchor="left",
            y=1,
            yanchor="top",
        )
    ],
)

fig.show()
