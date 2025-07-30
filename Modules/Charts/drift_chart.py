import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def semmantic_drift_plot_plotly(region, year, tf_dfs, tf_idfs,
                                 words=['generative ai', 'ai', 'machine learning', 'llm'],
                                 fz=12, debug=False):
    x_raw = tf_dfs[region][0][year]
    y_raw = tf_idfs[region][year]
    
    # Filter each Series independently to remove zero values
    x_nonzero = x_raw[x_raw > 0]
    y_nonzero = y_raw[y_raw > 0]
    
    # Find shared non-zero tokens
    common_index = x_nonzero.index.intersection(y_nonzero.index)
    
    # Subset both to aligned, valid entries
    x = x_raw.loc[common_index]
    y = y_raw.loc[common_index]

    if x.empty or y.empty:
        if debug:
            print(f"[DEBUG] Empty data for region: {region}, year: {year}")
        return go.Figure()

    x_thresh = np.percentile(x, 90)
    y_thresh = np.percentile(y, 90)

    fig = go.Figure()

    # Base Lexicon scatter
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        name='Lexicon',
        marker=dict(color='rgba(31, 119, 180, 0.5)', size=6),
        text=x.index,
        hovertemplate="<b>%{text}</b><br>TF=%{x}<br>TF-IDF=%{y}<extra></extra>"
    ))

    # Keyword highlights
    keyword_index = list(set(words).intersection(x.index))
    kw_x = x.loc[keyword_index]
    kw_y = y.loc[keyword_index]

    fig.add_trace(go.Scatter(
        x=kw_x, y=kw_y,
        mode='markers + text',
        name='Keywords',
        marker=dict(color='white', size=8, line=dict(color='red', width=1)),
        textfont=dict(color='red', size=fz-3, weight='bold'),
        text=[w.upper().replace(' ', '<br>') if ' ' in w else '<br><br>' + w.upper()  for w in keyword_index],
        hovertemplate="<b>%{text}</b><br>TF=%{x}<br>TF-IDF=%{y}<extra></extra>"
    ))

    # Quadrant lines
    fig.add_shape(type="line", x0=x_thresh, x1=x_thresh, y0=2**-7, y1=2**3,
                  line=dict(color="black", dash="dash", width=1.25))
    fig.add_shape(type="line", y0=y_thresh, y1=y_thresh, x0=2**-16, x1=2**-6,
                  line=dict(color="black", dash="dash", width=1.25))

    # Quadrant shading
    fig.add_shape(type="rect", x0=x_thresh, x1=2**-6, y0=y_thresh, y1=2**3,
                  fillcolor="#2ca02c", opacity=0.05, layer="below", line_width=0)
    fig.add_shape(type="rect", x0=2**-16, x1=x_thresh, y0=y_thresh, y1=2**3,
                  fillcolor="#ff7f0e", opacity=0.05, layer="below", line_width=0)
    fig.add_shape(type="rect", x0=x_thresh, x1=2**-6, y0=2**-7, y1=y_thresh,
                  fillcolor="#1f77b4", opacity=0.05, layer="below", line_width=0)
    fig.add_shape(type="rect", x0=2**-16, x1=x_thresh, y0=2**-7, y1=y_thresh,
                  fillcolor="#7f7f7f", opacity=0.05, layer="below", line_width=0)

    # Axis ticks: base-2 labels
    x_ticks = [2**i for i in range(-16, -5)]
    x_labels = [f"2^{i}" for i in range(-16, -5)]
    y_ticks = [2**i for i in range(-7, 3)]
    y_labels = [f"2^{i}" for i in range(-7, 3)]

    fig.update_xaxes(
    type='log',
    range=[np.log10(2**-16.5), np.log10(2**-6)],
        tickvals=x_ticks,
        ticktext=x_labels,
        title_text="←  Normalized TF  →",
    )
    fig.update_yaxes(
        type='log',
        range=[np.log10(2**-7), np.log10(2**3)],
        tickvals=y_ticks,
        ticktext=y_labels,
        title_text="←  TF-IDF  →",
    )

    fig.update_layout(
        title=f"{region.title()} {year}: TF vs TF-IDF (90th Percentile Thresholds)",
        template="simple_white",
        width=800,
        height=700,
        font=dict(size=fz),
        legend=dict(x=0.83, y=0.5),
        hovermode='closest'
    )

    # Quadrant titles
    fig.add_annotation(xref="paper", yref="paper", x=0.2, y=0.99, text="Rare but Telling",
                       font=dict(size=fz, color='#ff7f0e'), showarrow=False)
    fig.add_annotation(xref="paper", yref="paper", x=0.95, y=0.99, text="Frequent + Distinctive",
                       font=dict(size=fz, color='#2ca02c'), showarrow=False)
    fig.add_annotation(xref="paper", yref="paper", x=0.3, y=0.15, text="Noise",
                       font=dict(size=fz, color='#7f7f7f'), showarrow=False)
    fig.add_annotation(xref="paper", yref="paper", x=0.95, y=0.15, text="Generic but Common",
                       font=dict(size=fz, color='#1f77b4'), showarrow=False)

    # Axis-side labels
    fig.add_annotation(xref="paper", yref="paper", x=0.075, y=0.001,
                       text="Low<br>Frquency<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f'), align='center')
    fig.add_annotation(xref="paper", yref="paper", x=0.975, y=0.001,
                       text="High<br>Frquency<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f'), align='center')
    fig.add_annotation(xref="paper", yref="paper", x=0.0025, y=0.05,
                       text="Low<br>Distinctive<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f'), align='center', textangle=-90)
    fig.add_annotation(xref="paper", yref="paper", x=0.0025, y=0.99,
                       text="High<br>Distinctive<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f'), align='center', textangle=-90)

    return fig
