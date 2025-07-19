import numpy as np
from sentence_transformers import SentenceTransformer

def get_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    """
    Generates sentence embeddings for a list of strings using a pre-trained model.

    Parameters:
        texts (list of str): Text data to embed.
        model_name (str): Hugging Face model name.

    Returns:
        np.ndarray: Matrix of embeddings (n_samples, embedding_dim)
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings
