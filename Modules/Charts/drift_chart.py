import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st

def semmantic_drift_plot_plotly(region, year, tf_dfs, tf_idfs,
                                 words=['generative ai', 'ai', 'machine learning', 'llm']):
    """
    Generates a semantic drift scatter plot using Plotly, showing TF vs TF-IDF.
    This version is interactive and replicates the visual style of the Matplotlib chart.
    """

    if region not in tf_dfs or year not in tf_dfs[region][0].columns:
        return go.Figure()
    if region not in tf_idfs or year not in tf_idfs[region].columns:
        return go.Figure()

    tf_series = tf_dfs[region][0][year].copy()
    tfidf_series = tf_idfs[region][year].copy()

    # Handle zeros before log transform
    tf_series = tf_series.replace(0, 1e-20)
    tfidf_series = tfidf_series.replace(0, 1e-20)

    combined_df = pd.DataFrame({
        'tf': tf_series,
        'tfidf': tfidf_series
    }).dropna()

    x_thresh = np.percentile(combined_df['tf'], 90)
    y_thresh = np.percentile(combined_df['tfidf'], 90)

    fig = go.Figure()

    # Plot the scatter for the entire lexicon (blue)
    fig.add_trace(go.Scatter(
        x=combined_df['tf'],
        y=combined_df['tfidf'],
        mode='markers',
        marker=dict(color='Blue', opacity=0.5, size=8),
        name='Lexicon',
        hovertext=combined_df.index.tolist(),
        hovertemplate='<b>%{hovertext}</b><br>TF: %{x}<br>TF-IDF: %{y}<extra></extra>'
    ))

    # Plot the keywords (red)
    keywords_df = combined_df[combined_df.index.isin(words)]
    if not keywords_df.empty:
        fig.add_trace(go.Scatter(
            x=keywords_df['tf'],
            y=keywords_df['tfidf'],
            mode='markers',
            marker=dict(color='Red', opacity=0.8, size=10),
            name='Keywords',
            hovertext=keywords_df.index.tolist(),
            hovertemplate='<b>%{hovertext}</b><br>TF: %{x}<br>TF-IDF: %{y}<extra></extra>'
        ))

    # Add percentile-based quadrant lines (dashed black)
    fig.add_shape(type="line", x0=x_thresh, y0=combined_df['tfidf'].min(), x1=x_thresh, y1=combined_df['tfidf'].max(),
                  line=dict(color='black', dash='dash', width=1.5))
    fig.add_shape(type="line", x0=combined_df['tf'].min(), x1=combined_df['tf'].max(), y0=y_thresh, y1=y_thresh,
                  line=dict(color='black', dash='dash', width=1.5))

    # Add text annotations for keywords
    for word in words:
        if word in keywords_df.index:
            fig.add_annotation(
                x=keywords_df.loc[word, 'tf'],
                y=keywords_df.loc[word, 'tfidf'],
                text=word.upper().replace(' ', '<br>'),
                showarrow=True,
                font=dict(color="Red", size=9),
                arrowhead=1,
                ax=0, ay=-40,
                xanchor="center", yanchor="middle"
            )

    # Shaded quadrants using data coordinates
    tf_min, tf_max = combined_df['tf'].min(), combined_df['tf'].max()
    tfidf_min, tfidf_max = combined_df['tfidf'].min(), combined_df['tfidf'].max()

    fig.add_vrect(x0=x_thresh, x1=tf_max, xref='x',
                  y0=y_thresh, y1=tfidf_max, yref='y',
                  fillcolor='#2ca02c', opacity=0.05, layer="below")

    fig.add_vrect(x0=tf_min, x1=x_thresh, xref='x',
                  y0=y_thresh, y1=tfidf_max, yref='y',
                  fillcolor='#ff7f0e', opacity=0.05, layer="below")

    fig.add_vrect(x0=x_thresh, x1=tf_max, xref='x',
                  y0=tfidf_min, y1=y_thresh, yref='y',
                  fillcolor='#1f77b4', opacity=0.05, layer="below")

    fig.add_vrect(x0=tf_min, x1=x_thresh, xref='x',
                  y0=tfidf_min, y1=y_thresh, yref='y',
                  fillcolor='#7f7f7f', opacity=0.05, layer="below")

    # Layout updates
    fig.update_layout(
        title=f"{region.title()} {year}: TF vs TF-IDF (90th Percentile Thresholds)",
        xaxis_title="←  Normalized TF  →  ",
        yaxis_title="←  TF-IDF  →  ",
        xaxis_type='log',
        yaxis_type='log',
        xaxis=dict(range=[-16, -6]),  # You can make this dynamic if needed
        yaxis=dict(range=[-7, 2]),
        hovermode="closest",
        legend_title_text='Trace',
        template='plotly_white',
    )

    return fig
