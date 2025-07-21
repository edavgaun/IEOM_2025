import pandas as pd
import altair as alt

def get_top_terms(bow_df: pd.DataFrame, top_n=20):
    """
    Computes the top_n most frequent terms from a BoW matrix,
    always excluding the first three columns (e.g., 'Cleaned', 'Conference', 'Year').
    """
    bow_only = bow_df.iloc[:, 3:]  # Always skip the first 3 columns
    term_freq = bow_only.sum().sort_values(ascending=False).head(top_n)

    freq_df = term_freq.reset_index()
    freq_df.columns = ["Word", "Frequency"]
    return freq_df

def make_freq_chart(freq_df: pd.DataFrame, top_n=20, width=400, height=300):
    """
    Creates an Altair bar chart from a word frequency DataFrame.
    """
    return alt.Chart(freq_df).mark_bar().encode(
        x=alt.X("Word:N", sort="-y"),
        y=alt.Y("Frequency:Q"),
        tooltip=["Word", "Frequency"]
    ).properties(
        width=width,
        height=height,
        title=f"Top {top_n} Terms in BoW Matrix"
    )
