# Modules/Charts/drift_chart.py
import numpy as np
import pandas as pd
import streamlit as st

def semmantic_drift_plot_matplotlib(region, year, tf_dfs, tf_idfs,
                                     words=['generative ai', 'ai', 'machine learning', 'llm'],
                                     fz=12):
    """
    Generates a semantic drift scatter plot using Matplotlib, showing TF vs TF-IDF.

    Args:
        region (str): The region key (e.g., 'international', 'african', 'asia', 'north', etc).
        year (int): The year for which to plot the data.
        tf_dfs (dict): Dictionary containing Term Frequency DataFrames.
                       Expected format: {'region': [pd.DataFrame(tf_data)]}
        tf_idfs (dict): Dictionary containing TF-IDF DataFrames.
                        Expected format: {'region': pd.DataFrame(tfidf_data)}
        words (list): List of keywords to highlight on the plot.
        fz (int): Base font size for the plot elements.

    Returns:
        streamlit scatterplot
    """

    tf_series = tf_dfs[region][0][year]
    tfidf_series = tf_idfs[region][year]

    chart_data = pd.DataFrame(
    np.random.randn(20, 4), columns=["col1", "col2", "col3", "col4"]
    )
    
    st.scatter_chart(
        chart_data,
        x="col1",
        y=["col2", "col3"],
        size="col4",
        color=["#FF0000", "#0000FF"],  # Optional
    )
