# Modules/Charts/drift_chart.py
import matplotlib.pyplot as plt
import matplotlib.lines as mlines # Will be used for legend handles later
import numpy as np
import pandas as pd
import streamlit as st # Potentially for st.error, but the function should return a figure

def semmantic_drift_plot_matplotlib(region, year, tf_dfs, tf_idfs,
                                     words=['generative ai', 'ai', 'machine learning', 'llm'],
                                     fz=12):
    """
    Generates a semantic drift scatter plot using Matplotlib, showing TF vs TF-IDF.

    Args:
        region (str): The region key (e.g., 'annual', 'international').
        year (int): The year for which to plot the data.
        tf_dfs (dict): Dictionary containing Term Frequency DataFrames.
                       Expected format: {'region': [pd.DataFrame(tf_data)]}
        tf_idfs (dict): Dictionary containing TF-IDF DataFrames.
                        Expected format: {'region': pd.DataFrame(tfidf_data)}
        words (list): List of keywords to highlight on the plot.
        fz (int): Base font size for the plot elements.

    Returns:
        matplotlib.figure.Figure: The generated Matplotlib figure.
    """

    # --- 1. Data Preparation and Validation ---
    # (We'll add more data preparation here as we go, but start with validation)
    if region not in tf_dfs or year not in tf_dfs[region][0].columns:
        st.error(f"Data not found for region: '{region}' or year: '{year}' in TF data. Returning empty figure.")
        return plt.figure()
    if region not in tf_idfs or year not in tf_idfs[region].columns:
        st.error(f"Data not found for region: '{region}' or year: '{year}' in TF-IDF data. Returning empty figure.")
        return plt.figure()

    tf_series = tf_dfs[region][0][year]
    tfidf_series = tf_idfs[region][year]

    common_index = tf_series.index.intersection(tfidf_series.index)
    
    combined_df = pd.DataFrame({
        'tf': tf_series.loc[common_index],
        'tfidf': tfidf_series.loc[common_index]
    }).dropna()

    combined_df['word'] = combined_df.index.astype(str)
    
    # Ensure all values are strictly positive for log scales
    # Replace 0s with a very small number to avoid log(0) errors
    combined_df['tf'] = combined_df['tf'].replace(0, 1e-20) 
    combined_df['tfidf'] = combined_df['tfidf'].replace(0, 1e-20) 
    
    # Identify keywords for distinct styling and annotations
    combined_df['is_keyword'] = combined_df['word'].isin(words)
    present_keywords_df = combined_df[combined_df['is_keyword']].copy()


    # --- 2. Setup Figure and Axes ---
    fig, axs = plt.subplots(figsize=(10, 8)) # Create a figure and a set of subplots

    # Define the linear limits that correspond to your desired log2 limits
    x_min_linear = 2**-16
    x_max_linear = 2**-6
    y_min_linear = 2**-7
    y_max_linear = 2**2

    # Set log scale for both axes
    axs.set_xscale('log', base=2)
    axs.set_yscale('log', base=2)

    # Set explicit limits for the axes
    axs.set_xlim(x_min_linear, x_max_linear)
    axs.set_ylim(y_min_linear, y_max_linear)

    # --- (More plotting elements will go here) ---


    return fig # Return the figure object
