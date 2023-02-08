from sklearn.metrics.pairwise import cosine_similarity

import tensorflow as tf
import tensorflow_hub as hub
import sys
sys.path.insert(1, '/Users/adit/GameOfPapers')
from data_parser import get_docs , output_data


base_document, documents, doc_ids = get_docs()

def process_use_similarity():
	module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #@param ["https://tfhub.dev/google/universal-sentence-encoder/4", "https://tfhub.dev/google/universal-sentence-encoder-large/5"]


	model = hub.load(module_url)

	base_embeddings = model([base_document])

	embeddings = model(documents)

	scores = cosine_similarity(base_embeddings, embeddings).flatten()

	highest_score = 0
	highest_score_index = 0
	for i, score in enumerate(scores):
		if highest_score < score:
			highest_score = score
			highest_score_index = i

	most_similar_document = documents[highest_score_index]
	print("Most similar document by USE with the score:", most_similar_document, highest_score)

process_use_similarity()
