# Modules/Charts/drift_chart.py
import numpy as np
import pandas as pd
import streamlit as st

def semmantic_drift_plot(region, year, tf_dfs, tf_idfs,
                                     words=['generative ai', 'ai', 'machine learning', 'llm'],
                                     fz=12):
    """
    Generates a semantic drift scatter plot using Matplotlib, showing TF vs TF-IDF.

    Args:
        region (str): The region key (e.g., 'international', 'african', 'asia', 'north', etc).
        year (int): The year for which to plot the data.
        tf_dfs (dict): Dictionary containing Term Frequency DataFrames.
        tf_idfs (dict): Dictionary containing TF-IDF DataFrames.
        words (list): List of keywords to highlight on the plot.
        fz (int): Base font size for the plot elements.

    Returns:
        streamlit scatterplot
    """

    tf_series = tf_dfs[region][0][year]
    tfidf_series = tf_idfs[region][year]

    # --- THE FIX STARTS HERE ---
    # Create the chart_data DataFrame from the two series
    chart_data = pd.DataFrame({
        'tf_values': tf_series,
        'tfidf_values': tfidf_series
    }).dropna()
    
    # Identify the keywords for coloring
    chart_data['is_keyword'] = chart_data.index.isin(words)
    
    # --- Corrected st.scatter_chart call ---
    st.scatter_chart(
        chart_data,
        x="tf_values",
        y="tfidf_values",
        color="is_keyword",
    )
