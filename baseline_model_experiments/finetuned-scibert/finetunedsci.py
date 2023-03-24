from collections import OrderedDict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk import sent_tokenize
import nltk
from sentence_transformers import SentenceTransformer
import json
import sys
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForNextSentencePrediction
from transformers import AutoModel, AutoTokenizer

    # caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/Users/adit/GameOfPapers')
from baseline_model_experiments.data_parser import get_docs
# Opening JSON file

  
# returns JSON object as 
# a dictionary
base_document, documents, doc_ids = get_docs()
print(base_document)
#nltk.download('punkt')
def process_bert_similarity():
    # This will download and load the pretrained model offered by UKPLab.
    pretrained = 'allenai/scibert_scivocab_uncased'
    finetuned = '/Users/adit/GameOfPapers/bert-based-triplet/ckpt/scibert_model_v6_triplet_2.pt'

    #model = SentenceTransformer(pretrained)
    model = AutoModel.from_pretrained(pretrained)
    state_dict = torch.load(finetuned)
    state_dict = OrderedDict([(k.replace("bert.",""),v) for k, v in state_dict.items()])
    del state_dict['space_joiner.out1.weight']
    del state_dict["space_joiner.out1.bias"]
    del state_dict["space_joiner.out2.weight"] 
    del state_dict["space_joiner.out2.bias"]
    model.load_state_dict(state_dict)
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")



    # Although it is not explicitly stated in the official document of sentence transformer, 
    # the original BERT is meant for a shorter sentence. We will feed the model by sentences instead of the whole documents.
    tokens = tokenizer([base_document], padding=True, truncation=True, return_tensors="pt", max_length=500)

    with torch.no_grad():
        outputs = model(**tokens)
        base_embeddings_sentences = outputs.last_hidden_state.mean(dim=1)
    base_embeddings = np.mean(np.array(base_embeddings_sentences), axis=0)

    vectors = []

    for i, document in enumerate(documents):

        
        tokens = tokenizer(document, padding=True, truncation=True, return_tensors="pt", max_length=500)
        with torch.no_grad():

            outputs = model(**tokens)
            embeddings_sentences = outputs.last_hidden_state.mean(dim=1)
            
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

process_bert_similarity()