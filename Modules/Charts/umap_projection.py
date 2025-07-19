import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import umap

def get_umap_projection(embeddings: np.ndarray, n_components_pca: int = 120, random_state: int = 42):
    """
    Reduce high-dimensional embeddings to 2D using PCA followed by UMAP.

    Parameters
    ----------
    embeddings : np.ndarray
        Original high-dimensional vector representations.
    n_components_pca : int
        Number of PCA components to retain before UMAP.
    random_state : int
        Random seed for UMAP reproducibility.

    Returns
    -------
    np.ndarray
        2D UMAP projection of the embeddings.
    """
    pca_data = PCA(n_components=n_components_pca).fit_transform(embeddings)
    reducer = umap.UMAP(n_components=2, random_state=random_state)
    embedding_2d = reducer.fit_transform(pca_data)
    return embedding_2d
