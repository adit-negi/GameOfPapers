import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk import sent_tokenize
import nltk
from sentence_transformers import SentenceTransformer
import json
import sys
from torch import nn
    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/Users/adit/GameOfPapers')
from data_parser import get_thousand_papers 
# Opening JSON file
from transformers import *

tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')
  
# returns JSON object as 
# a dictionary
data = get_thousand_papers()
i = 0
documents = []
doc_ids = []
for doc_id in data:
	if i==0:
		base_document = doc_id['title'] +" " + doc_id['abstract']
		i = i+1
	else:
		documents.append(doc_id['title'] +" " + doc_id['abstract'])
		doc_ids.append((doc_id['id'], doc_id['categories']))

print(base_document)
#nltk.download('punkt')
def process_scibert_similarity():
    # This will download and load the pretrained model offered by UKPLab.


    # Although it is not explicitly stated in the official document of sentence transformer, the original BERT is meant for a shorter sentence. We will feed the model by sentences instead of the whole documents.
    sentences = sent_tokenize(base_document)
    base_embeddings_sentences = model(**tokenizer(sentences, padding=True, truncation=True, max_length=512, return_tensors="pt"))
    print(base_embeddings_sentences)
    base_embeddings = nn.functional.softmax(base_embeddings_sentences.logits, dim=-1)

    vectors = []
    for i, document in enumerate(documents):

        sentences = sent_tokenize(document)
        embeddings_sentences = model(tokenizer(sentences, padding=True, truncation=True, max_length=512))
        embeddings = np.mean(np.array(embeddings_sentences), axis=0)

        vectors.append(embeddings)

        print("making vector at index:", i)

    scores = cosine_similarity([base_embeddings], vectors).flatten()
    output = []
    for i in range(len(scores)):
        output.append((scores[i], documents[i], doc_ids[i][0],doc_ids[i][1] ))
    output.sort(reverse=True)

    d= {}
    for i, j,l,k in output:
        
        d[str(i)] = [j,l,k]
    json_object = json.dumps(d, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    highest_score = 0
    highest_score_index = 0
    for i, score in enumerate(scores):
        if highest_score < score:
            highest_score = score
            highest_score_index = i

    most_similar_document = documents[highest_score_index]
    print("Most similar document by BERT with the score:", most_similar_document, highest_score)

process_scibert_similarity()
