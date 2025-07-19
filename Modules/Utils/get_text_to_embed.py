import pandas as pd

def prepare_text(df, method="title"):
    """
    Adds a column 'text_to_embed' to the DataFrame, based on the selected method.
    Options: 'title', 'abstract', 'title+keywords'
    """
    if method == "title":
        df["text_to_embed"] = df["Title"]
    elif method == "abstract":
        df["text_to_embed"] = df["Abstract"]
    elif method == "title+keywords":
        df["text_to_embed"] = df["Title"].fillna('') + " " + df["Keywords"].fillna('')
    else:
        raise ValueError(f"Unknown method '{method}'. Choose from 'title', 'abstract', or 'title+keywords'.")
    return df
