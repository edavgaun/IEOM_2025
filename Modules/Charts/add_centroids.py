import plotly.graph_objects as go
import pandas as pd

def add_centroids_to_umap(fig, df, x_col="x", y_col="y", year_col="Year", rug_length=0.3):
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

    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with centroid crosses, labels, and rug ticks.
    """
    # Get color mapping from original scatter plot traces
    year_colors = {}
    for trace in fig.data:
        if trace.name:
            year = trace.name.strip()
            year_colors[year] = trace.marker.color

    # Define reference axis minimums (used for rug placement)
    x0 = df[x_col].min()
    y0 = df[y_col].min()

    # Compute and add centroid traces
    for year in df[year_col].unique():
        sub_df = df[df[year_col] == year]
        if len(sub_df) == 0:
            continue

        centroid_x = sub_df[x_col].mean()
        centroid_y = sub_df[y_col].mean()
        color = year_colors.get(str(year), "black")

        # Centroid marker with label
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

        # Rug line on x-axis (vertical tick)
        fig.add_trace(go.Scatter(
            x=[centroid_x, centroid_x],
            y=[y0, y0 + rug_length],
            mode="lines",
            line=dict(color=color, width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

        # Rug line on y-axis (horizontal tick)
        fig.add_trace(go.Scatter(
            x=[x0, x0 + rug_length],
            y=[centroid_y, centroid_y],
            mode="lines",
            line=dict(color=color, width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

    return fig
