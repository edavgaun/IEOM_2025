import plotly.graph_objects as go
import pandas as pd

def add_centroids_to_umap(fig, df, x_col="x", y_col="y", year_col="Year", padding=0.5):
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

    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with vertical lines and properly rotated year labels.
    """
    # Get colors from existing figure
    year_colors = {}
    for trace in fig.data:
        if trace.name:
            year = trace.name.strip()
            year_colors[year] = trace.marker.color

    # Y-axis range for dashed line and label height
    y_range = fig.layout.yaxis.range or [df[y_col].min(), df[y_col].max()]
    y_min, y_max = y_range[0], y_range[1]
    label_y = y_max + padding

    for year in df[year_col].unique():
        sub_df = df[df[year_col] == year]
        if sub_df.empty:
            continue

        centroid_x = sub_df[x_col].mean()
        color = year_colors.get(str(year), "black")

        # Add vertical dashed line
        fig.add_shape(
            type="line",
            x0=centroid_x,
            x1=centroid_x,
            y0=y_min,
            y1=y_max,
            line=dict(color=color, width=2, dash="dash"),
            layer="below"
        )

        # Add vertical label using annotation
        fig.add_annotation(
            x=centroid_x,
            y=label_y,
            text=str(year),
            showarrow=False,
            textangle=90,
            font=dict(color=color, size=12),
            xanchor="center",
            yanchor="bottom"
        )

    return fig
