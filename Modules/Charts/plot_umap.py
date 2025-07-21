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

def plot_umap_scatter(df, selected_years=None, selected_conferences=None, selected_topics=None):
    df = filter_df(df, selected_years, selected_conferences, selected_topics)
    df["Year"] = df["Year"].astype(str)

    # Get list of visible topics after filtering
    visible_topics = df["FinalTopicName"].unique()

    # Define full color map
    full_color_map = {
        "Outliers / Uncategorized": "#d3d3d3",
        "Maintenance & Reliability Engineering": "#1f77b4",
        "Sustainability & Green Supply Chains": "#ff7f0e",
        "Industry 4.0 & Smart Manufacturing": "#2ca02c",
        "Project & Construction Management": "#9467bd",
        "Innovation & Entrepreneurship": "#8c564b",
        "Machine Learning Methods": "#e377c2",
        "Employee Behavior & Job Performance": "#17becf",
        "3D Printing & Surface Engineering": "#7f7f7f",
        "Renewable Energy & Power Systems": "#bcbd22",
        "Vehicle Routing & Optimization Problems": "#4b0082",
        "Ergonomics & Worker Safety": "#ff1493",
        "TQM, ISO & Quality Management": "#6a3d9a",
        "Inventory Control & Demand Forecasting": "#ffcc00",
        "Public Policy & Government Programs": "#009e73",
        "Learning, Students & Education": "#e41a1c",
        "Lean Six Sigma & DMAIC": "#377eb8",
        "Customer Experience & Brand Perception": "#f781bf",
        "Supply Chain & Risk Assessment": "#a65628",
        "Financial Markets & Corporate Finance": "#984ea3"
    }

    # Restrict color map to visible topics
    filtered_color_map = {topic: full_color_map.get(topic, "#888888") for topic in visible_topics}

    fig = px.scatter(
        df,
        x="x",
        y="y",
        color="FinalTopicName",
        color_discrete_map=filtered_color_map,
        hover_data={"Title": True, "Year": True, "x": False, "y":False, 'Conference':True},
        opacity=0.6
    )

    # 🧠 Your original layout preserved
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
