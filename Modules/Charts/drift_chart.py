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

    # Extract x and y for that region and year
    x = tf_dfs[region][0][year]
    y = tf_idfs[region][year]
  
    # Compute percentiles using only this region
    x_thresh = np.percentile(x, 90)
    y_thresh = np.percentile(y, 90)
    
    st.scatter_chart(
        x=x,
        y=y,
        color=["#FF0000"],
    )
