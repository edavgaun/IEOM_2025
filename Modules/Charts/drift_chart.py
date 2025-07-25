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
    chart_data['word'] = chart_data.index # Move the word from index to a column

    # The colors must be provided as a list for vega_lite_chart
    color_map = {True: '#FF0000', False: '#ADD8E6'}
    chart_data['color_coding'] = chart_data['is_keyword'].map(color_map)
    
    # --- The Vega-Lite Specification ---
    spec = {
        "mark": "point",
        "encoding": {
            "x": {
                "field": "tf_values",
                "type": "quantitative",
                "axis": {"title": "Normalized TF"},
                "scale": {"type": "log", "base": 2, "domain": [1e-6, 0.05]}
            },
            "y": {
                "field": "tfidf_values",
                "type": "quantitative",
                "axis": {"title": "TF-IDF"},
                "scale": {"type": "log", "base": 2, "domain": [1e-3, 4]}
            },
            "color": {
                "field": "color_coding",
                "type": "nominal",
                "scale": {"domain": ["#FF0000", "#ADD8E6"], "range": ["#FF0000", "#ADD8E6"]}
            },
            # --- The Hover Tooltip ---
            "tooltip": [
                {"field": "word", "type": "nominal", "title": "Word"}
            ]
        }
    }

    st.vega_lite_chart(chart_data, spec)
