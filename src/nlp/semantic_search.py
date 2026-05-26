import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from nlp.embedding_pipeline import (
    generate_embeddings
)


def semantic_search(
    query,
    texts,
    top_k=5
):

    query_embedding = (
        generate_embeddings([query])
    )

    text_embeddings = (
        generate_embeddings(texts)
    )

    similarities = cosine_similarity(
        query_embedding,
        text_embeddings
    )[0]

    top_indices = np.argsort(
        similarities
    )[::-1][:top_k]

    results = []

    for idx in top_indices:

        results.append({

            "text": texts[idx],

            "similarity_score": float(
                similarities[idx]
            )
        })

    return results