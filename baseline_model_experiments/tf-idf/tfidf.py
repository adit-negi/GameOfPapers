from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.insert(1, '/Users/adit/GameOfPapers')
from baseline_model_experiments.data_parser import get_docs , output_data

base_document, documents, doc_ids = get_docs()

def process_tfidf_similarity():
    vectorizer = TfidfVectorizer()
    # To make uniformed vectors, both documents need to be combined first.
    print(base_document)
    documents.insert(0, base_document)
    embeddings = vectorizer.fit_transform(documents)

    cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()

    highest_score = 0
    highest_score_index = 0
    for i, score in enumerate(cosine_similarities):
        if highest_score < score:
            highest_score = score
            highest_score_index = i


    json_object = output_data(cosine_similarities, documents, doc_ids)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    most_similar_document = documents[highest_score_index]

    print("Most similar document by TF-IDF with the score:", most_similar_document, highest_score)

process_tfidf_similarity()
