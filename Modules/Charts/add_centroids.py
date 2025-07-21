import plotly.graph_objects as go
import pandas as pd

def add_centroids_to_umap(fig, df, x_col="x", y_col="y", year_col="Year", padding=0.5):
    """
    Add vertical dashed lines at centroid x-positions with vertically rotated year labels.

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
        Distance above the top of y-axis where the label will appear.

    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with vertical dashed lines and rotated year labels.
    """
    # Extract year-color mapping from original traces
    year_colors = {}
    for trace in fig.data:
        if trace.name:
            year = trace.name.strip()
            year_colors[year] = trace.marker.color

    # Get y-axis range for vertical line span and label position
    y_range = fig.layout.yaxis.range or [df[y_col].min(), df[y_col].max()]
    y_bottom, y_top = y_range[0], y_range[1]
    label_y = y_top + padding

    for year in df[year_col].unique():
        sub_df = df[df[year_col] == year]
        if len(sub_df) == 0:
            continue

        centroid_x = sub_df[x_col].mean()
        color = year_colors.get(str(year), "black")

        # Add vertical dashed line
        fig.add_trace(go.Scatter(
            x=[centroid_x, centroid_x],
            y=[y_bottom, y_top],
            mode="lines",
            line=dict(color=color, width=2, dash="dash"),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Add vertical year label (rotated)
        fig.add_trace(go.Scatter(
            x=[centroid_x],
            y=[label_y],
            mode="markers+text",
            marker=dict(opacity=0),
            text=[str(year)],
            textangle=90,
            textposition="top center",
            textfont=dict(color=color, size=12),
            showlegend=False,
            hoverinfo="skip"
        ))

    return fig
