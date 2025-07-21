import plotly.graph_objects as go
import pandas as pd

def add_centroids_to_umap(fig, df, x_col="x", y_col="y", year_col="Year", rug_length=0.3, padding=0.5):
    """
    Add centroid markers with year labels and rug lines to an existing Plotly UMAP figure.

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
    rug_length : float
        Length of the rug ticks on the axes.
    padding : float
        Distance outside the plot area where rug ticks are placed.

    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with centroid crosses, labels, and rug ticks.
    """
    # Extract color mapping from original scatterplot traces
    year_colors = {}
    for trace in fig.data:
        if trace.name:
            year = trace.name.strip()
            year_colors[year] = trace.marker.color

    # Get axis ranges (fallback to data-based ranges if layout not yet populated)
    x_range = fig.layout.xaxis.range or [df[x_col].min(), df[x_col].max()]
    y_range = fig.layout.yaxis.range or [df[y_col].min(), df[y_col].max()]
    
    x_rug_base = y_range[0] - padding
    y_rug_base = x_range[0] - padding

    # Compute and add centroid markers and rug ticks
    for year in df[year_col].unique():
        sub_df = df[df[year_col] == year]
        if len(sub_df) == 0:
            continue

        centroid_x = sub_df[x_col].mean()
        centroid_y = sub_df[y_col].mean()
        color = year_colors.get(str(year), "black")

        # Centroid cross with label
        fig.add_trace(go.Scatter(
            x=[centroid_x],
            y=[centroid_y],
            mode="markers+text",
            marker=dict(symbol="x", size=16, color=color, line=dict(width=2)),
            text=[year],
            textposition="top center",
            textfont=dict(color=color, size=12),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Vertical rug tick (x-axis)
        fig.add_trace(go.Scatter(
            x=[centroid_x, centroid_x],
            y=[x_rug_base, x_rug_base + rug_length],
            mode="lines",
            line=dict(color=color, width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Horizontal rug tick (y-axis)
        fig.add_trace(go.Scatter(
            x=[y_rug_base, y_rug_base + rug_length],
            y=[centroid_y, centroid_y],
            mode="lines",
            line=dict(color=color, width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

    return fig
