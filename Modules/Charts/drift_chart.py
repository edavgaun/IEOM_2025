import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def semmantic_drift_plot_plotly(region, year, tf_dfs, tf_idfs,
                          words=['generative ai', 'ai', 'machine learning', 'llm'],
                          fz=12):
    # Extract data
    x = tf_dfs[region][0][year].replace(0, 1e-20)
    y = tf_idfs[region][year].replace(0, 1e-20)

    x_thresh = np.percentile(x, 90)
    y_thresh = np.percentile(y, 90)

    fig = go.Figure()

    # Lexicon
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='markers',
        name='Lexicon',
        marker=dict(color='rgba(31, 119, 180, 0.5)', size=6),
        text=x.index,
        hovertemplate="<b>%{text}</b><br>TF=%{x}<br>TF-IDF=%{y}<extra></extra>"
    ))

    # Keywords
    kw_x = x.loc[x.index.intersection(words)]
    kw_y = y.loc[y.index.intersection(words)]

    fig.add_trace(go.Scatter(
        x=kw_x, y=kw_y,
        mode='markers+text',
        name='Keywords',
        marker=dict(color='Red', size=9),
        text=[w.upper().replace(' ', '\n') for w in kw_x.index],
        textposition='top center',
        hovertemplate="<b>%{text}</b><br>TF=%{x}<br>TF-IDF=%{y}<extra></extra>"
    ))

    # Annotated arrows for keywords
    for i, word in enumerate(words):
        if word in kw_x.index:
            fig.add_annotation(
                x=kw_x[word],
                y=kw_y[word],
                ax=kw_x[word] + ((-1)**(i+1)) * 2**-7,
                ay=kw_y[word] + ((-1)**i) * 2**-5,
                text=word.upper().replace(' ', '<br>'),
                showarrow=True,
                arrowhead=1,
                arrowsize=1,
                arrowwidth=1.5,
                arrowcolor='red',
                font=dict(color='red', size=fz-2),
                align='center'
            )

    # Quadrant lines
    fig.add_shape(type="line", x0=x_thresh, x1=x_thresh, y0=2**-7, y1=2**2,
                  line=dict(color="black", dash="dash", width=1.25))
    fig.add_shape(type="line", y0=y_thresh, y1=y_thresh, x0=2**-16, x1=2**-6,
                  line=dict(color="black", dash="dash", width=1.25))

    # Shaded quadrants
    fig.add_shape(type="rect", x0=x_thresh, x1=2**-6, y0=y_thresh, y1=2**2,
                  fillcolor="#2ca02c", opacity=0.05, layer="below", line_width=0)
    fig.add_shape(type="rect", x0=2**-16, x1=x_thresh, y0=y_thresh, y1=2**2,
                  fillcolor="#ff7f0e", opacity=0.05, layer="below", line_width=0)
    fig.add_shape(type="rect", x0=x_thresh, x1=2**-6, y0=2**-7, y1=y_thresh,
                  fillcolor="#1f77b4", opacity=0.05, layer="below", line_width=0)
    fig.add_shape(type="rect", x0=2**-16, x1=x_thresh, y0=2**-7, y1=y_thresh,
                  fillcolor="#7f7f7f", opacity=0.05, layer="below", line_width=0)

    # Axis config
    fig.update_xaxes(
        type='log', title_text="←  Normalized TF  →",
        range=[np.log2(2**-16), np.log2(2**-6)],
        tickvals=[2**i for i in range(-16, -5)],
        tickformat=".1e"
    )
    fig.update_yaxes(
        type='log', title_text="←  TF-IDF  →",
        range=[np.log2(2**-7), np.log2(2**2)],
        tickvals=[2**i for i in range(-7, 3)],
        tickformat=".1e"
    )

    # Titles and quadrant labels
    fig.update_layout(
        title=f"Annual {year}: TF vs TF-IDF (90th Percentile Thresholds)",
        template="simple_white",
        legend=dict(x=0.85, y=0.05),
        font=dict(size=fz),
        width=800,
        height=700
    )

    # Quadrant labels
    fig.add_annotation(xref="paper", yref="paper", x=0.13, y=0.86, text="Rare but Telling",
                       font=dict(size=fz, color='#ff7f0e', family='Arial'), showarrow=False)
    fig.add_annotation(xref="paper", yref="paper", x=0.87, y=0.86, text="Frequent + Distinctive",
                       font=dict(size=fz, color='#2ca02c', family='Arial'), showarrow=False)
    fig.add_annotation(xref="paper", yref="paper", x=0.13, y=0.11, text="Noise",
                       font=dict(size=fz, color='#7f7f7f', family='Arial'), showarrow=False)
    fig.add_annotation(xref="paper", yref="paper", x=0.87, y=0.11, text="Generic but Common",
                       font=dict(size=fz, color='#1f77b4', family='Arial'), showarrow=False)

    # Corner labels (italic)
    fig.add_annotation(xref="paper", yref="paper", x=0.125, y=0.005,
                       text="Low<br>Frquency<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f', family='Arial'), align='center')
    fig.add_annotation(xref="paper", yref="paper", x=0.875, y=0.005,
                       text="High<br>Frquency<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f', family='Arial'), align='center')
    fig.add_annotation(xref="paper", yref="paper", x=0.04, y=0.08,
                       text="Low<br>Distinctive<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f', family='Arial'), align='center', textangle=-90)
    fig.add_annotation(xref="paper", yref="paper", x=0.05, y=0.85,
                       text="High<br>Distinctive<br>Tokens", showarrow=False,
                       font=dict(size=fz-2, color='#7f7f7f', family='Arial'), align='center', textangle=-90)

    return fig
