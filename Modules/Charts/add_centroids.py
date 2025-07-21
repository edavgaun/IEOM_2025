import plotly.graph_objects as go
import pandas as pd

def add_centroids_to_umap(
    fig,
    df,
    x_col="x",
    y_col="y",
    year_col="Year",
    padding=0.5,
    line_color="#cccccc",
    line_style="dot",
    line_width=1,
    text_color="#999999"
):
    """
    Add vertical dashed lines at centroid x-positions and label them with vertical year annotations.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The existing figure to be updated.
    df : pd.DataFrame
        DataFrame used for the UMAP plot.
    x_col : str
        Column name for the x-axis UMAP coordinate.
    y_col : str
        Column name for the y-axis UMAP coordinate.
    year_col : str
        Column name for the year grouping.
    padding : float
        Vertical space above the plot used to place the year labels.
    line_color : str
        Hex code for the vertical line color (e.g. "#cccccc").
    line_style : str
        Dash style for the line (e.g. "dot", "dash", "solid").
    line_width : int
        Line thickness.
    text_color : str
        Color for the year label text.

    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with vertical lines and year annotations.
    """
    # Determine Y-axis range (used for vertical lines and label placement)
    y_range = fig.layout.yaxis.range or [df[y_col].min(), df[y_col].max()]
    y_min, y_max = y_range[0], y_range[1]
    label_y = y_max + padding
    Xmax=0.775

    # Iterate through unique years and plot vertical dashed lines + labels
    for year in sorted(df[year_col].unique()):
        sub_df = df[df[year_col] == year]
        if sub_df.empty:
            continue

        centroid_x = sub_df[x_col].mean()
        Xmax=max(0.775, centroid_x)

        # Add vertical dashed line
        fig.add_shape(
            type="line",
            x0=centroid_x,
            x1=centroid_x,
            y0=y_min,
            y1=y_max,
            line=dict(color=line_color, width=line_width, dash=line_style),
            layer="below"
        )

        # Add vertical rotated label
        fig.add_annotation(
            x=centroid_x,
            y=label_y,
            text=str(year),
            showarrow=False,
            textangle=90,
            font=dict(color=text_color, size=11),
            xanchor="center",
            yanchor="bottom"
        )
        fig.add_annotation(
        xref="paper",
        yref="paper",
        x=max(0.5, Xmax),
        y=1.01,
        text=(
        "Dashed lines show the average position of <br>"
        " ← papers per year(semantic centroid),<br>" 
        "illustrating how topics shift over time."
        ),
        showarrow=False,
        font=dict(size=12, color="black"),
        align="center"
        )

    return fig
