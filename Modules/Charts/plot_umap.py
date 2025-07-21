import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def filter_df(df, selected_years, selected_conferences):
    return df[df["Year"].isin(selected_years) & df["Conference"].isin(selected_conferences)]

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
        Interactive scatterplot with year centroids.
    """
    df = filter_df(df, selected_years, selected_conferences)
    df["Year"] = df["Year"].astype(str)

    # Base scatterplot
    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="Year",
        hover_data={"x": False, "y": False, "Title": True, "Conference": True, "Year": True},
        opacity=0.65
    )

    # Extract the color mapping used by px
    color_map = fig.layout.coloraxis.colorbar.ticktext if 'coloraxis' in fig.layout else None
    if 'coloraxis' in fig.layout:
        fig.update_traces(marker=dict(color=None))  # Reset legacy color if needed

    # Manual color assignment (more reliable for newer px versions)
    year_colors = {trace.name: trace.marker.color for trace in fig.data if trace.name}

    # Compute and add centroid markers
    for year in df["Year"].unique():
        sub_df = df[df["Year"] == year]
        if len(sub_df) == 0:
            continue
        centroid_x = sub_df["x"].mean()
        centroid_y = sub_df["y"].mean()
        color = year_colors.get(year, "black")  # fallback color if not found

        fig.add_trace(go.Scatter(
            x=[centroid_x],
            y=[centroid_y],
            mode="markers+text",
            marker=dict(symbol="x", size=14, color=color),
            text=[year],
            textposition="top center",
            showlegend=False,
            hoverinfo="skip"
        ))

    fig.update_layout(
        title="UMAP Projection of IEOM Papers Across Conference Regions and Years",
        legend_title_text="Year",
        xaxis_title="UMAP-1",
        yaxis_title="UMAP-2"
    )
    return fig
