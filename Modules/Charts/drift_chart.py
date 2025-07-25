# Modules/Charts/drift_chart.py
import numpy as np
import pandas as pd
import streamlit as st

def semmantic_drift_plot(region, year, tf_dfs, tf_idfs,
                         words=['generative ai', 'ai', 'machine learning', 'llm']):

    tf_series = tf_dfs[region][0][year]
    tfidf_series = tf_idfs[region][year]
    
    chart_data = pd.DataFrame({
        'tf_values': tf_series,
        'tfidf_values': tfidf_series
    }).dropna()

    keywords_lower = [w.lower() for w in words]
    chart_data['is_keyword'] = chart_data.index.str.lower().isin(keywords_lower)

    color_map = {True: '#FF0000', False: '#1f77b4'}
    chart_data['color_coding'] = chart_data['is_keyword'].map(color_map)

    # --- Apply the log2 transformation ---
    chart_data['tf_values_log2'] = np.log2(chart_data['tf_values'].replace(0, 1e-20))
    chart_data['tfidf_values_log2'] = np.log2(chart_data['tfidf_values'].replace(0, 1e-20))

    # Define the axis ranges for the LOG-TRANSFORMED data
    x_config = st.column_config.NumberColumn(
        label="Log2(tf_values)",
        min_value=-16,
        max_value=-5
    )
    
    y_config = st.column_config.NumberColumn(
        label="Log2(tfidf_values)",
        min_value=-8,
        max_value=2
    )
    
    st.scatter_chart(
        chart_data,
        x=x_config,
        y=y_config,
        color="color_coding",
    )
