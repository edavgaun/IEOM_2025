import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def filter_df(df, selected_years, selected_conferences, selected_topics):
    return df[
        df["Year"].isin(selected_years) &
        df["Conference"].isin(selected_conferences) &
        df["FinalTopicName"].isin(selected_topics)
    ]

def plot_umap_scatter(
    df: pd.DataFrame,
    selected_years=None,
    selected_conferences=None,
    selected_topics=None
):
    """
    Plot a 2D UMAP scatterplot with filtering and hover features.
    """
    df = filter_df(df, selected_years, selected_conferences, selected_topics)
    df["Year"] = df["Year"].astype(str)

    # Define custom color palette (first is light gray for outliers)
    custom_colors = [
        "#d3d3d3",  # 0 - Light gray (Outliers)
        "#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b",
        "#e377c2", "#17becf", "#bcbd22", "#7f7f7f", "#4b0082",
        "#ff1493", "#6a3d9a", "#ffcc00", "#009e73", "#e41a1c",
        "#377eb8", "#f781bf", "#a65628", "#984ea3"
    ]

    # Ensure "Outliers / Uncategorized" appears first in the color ordering
    ordered_topics = sorted(
        df["FinalTopicName"].unique(),
        key=lambda x: (x != "Outliers / Uncategorized", x)
    )
    df["FinalTopicName"] = pd.Categorical(df["FinalTopicName"], categories=ordered_topics, ordered=True)

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="FinalTopicName",
        color_discrete_sequence=custom_colors,
        hover_data={
            "x": False, "y": False,
            "Title": True,
            "Conference": True,
            "Year": True,
            "Topic": True
        },
        opacity=0.65
    )

    fig.update_layout(
        height=800,
        title=(
            "UMAP Projection of IEOM Papers by Thematic Clusters"
            "<br><span style='font-size:14px; font-weight:normal'>"
            "(Use the toolbar at the top-right corner to zoom, pan, and explore → )"
            "</span>"
        ),
        legend_title="Topic",
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        plot_bgcolor="white"
    )

    return fig, df
