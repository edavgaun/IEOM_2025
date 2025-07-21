import plotly.graph_objects as go
import pandas as pd

def add_centroids_to_umap(fig, df, x_col="x", y_col="y", year_col="Year"):
    """
    Add centroid markers with year labels to an existing Plotly UMAP figure.

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

    Returns
    -------
    plotly.graph_objects.Figure
        Updated figure with centroid crosses and static labels.
    """
    # Get color mapping from existing traces
    year_colors = {}
    for trace in fig.data:
        if trace.name:
            year = trace.name.strip()
            year_colors[year] = trace.marker.color
        
    # Compute centroids per year
    for year in df[year_col].unique():
        sub_df = df[df[year_col] == year]
        if len(sub_df) == 0:
            continue

        centroid_x = sub_df[x_col].mean()
        centroid_y = sub_df[y_col].mean()

        # Try to find color
        color = year_colors.get(str(year), "black")

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

    return fig
