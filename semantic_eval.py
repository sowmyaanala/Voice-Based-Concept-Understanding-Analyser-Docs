from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(transcript, expected):
    emb1 = model.encode([transcript])
    emb2 = model.encode([expected])
    return cosine_similarity(emb1, emb2)[0][0]

if __name__ == "__main__":
    transcript = "Artificial Intelligence is the simulation of human intelligence."
    expected = "Artificial Intelligence is the simulation of human intelligence."

    score = semantic_similarity(transcript, expected)
    print("Similarity Score:", score)