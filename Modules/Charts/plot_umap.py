import pandas as pd
import plotly.express as px

def plot_umap_scatter(
    df: pd.DataFrame,
    selected_years=None,
    selected_conferences=None
):
    """
    Plot a 2D UMAP scatterplot with filtering and hover features.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame that includes UMAP coordinates 'x', 'y', 'Year', 'Title', 'Conference'.
    selected_years : list[int], optional
        List of years to include.
    selected_conferences : list[str], optional
        List of conference names to include.

    Returns
    -------
    plotly.graph_objects.Figure
        Interactive scatterplot.
    """
    if selected_years:
        df = df[df["Year"].isin(selected_years)]

    if selected_conferences:
        df = df[df["Conference"].isin(selected_conferences)]

    df = df.copy()
    df["Year"] = df["Year"].astype(str)

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="Year",
        hover_data={"x": False, "y": False, "Title": True, "Conference": True, "Year": True},
        opacity=0.65
    )
    fig.update_layout(
        title="UMAP Projection of IEOM Papers",
        legend_title_text="Year and Conference",
        xaxis_title="UMAP-1",
        yaxis_title="UMAP-2"
    )
    return fig
