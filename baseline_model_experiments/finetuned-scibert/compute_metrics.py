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
def get_documents():
    documents = json.loads(open('/Users/adit/GameOfPapers/scripts/samir.json').read())
    doc_ids, docs = {}, []
    for i in documents:
        
        docs.append(i['title']+" "+i['abstract'])
        doc_ids[i['title']+" "+i['abstract']] = i['internal_id']
    return docs, doc_ids


documents, doc_ids = get_documents()
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
    

    vectors = []
    results = {}
    for i, document in enumerate(documents):

        
        tokens = tokenizer(document, padding=True, truncation=True, return_tensors="pt", max_length=500)
        with torch.no_grad():

            outputs = model(**tokens)
            embeddings_sentences = outputs.last_hidden_state.mean(dim=1)
            
        embeddings = np.mean(np.array(embeddings_sentences), axis=0)

        vectors.append(embeddings)

        print("making vector at index:", i)

    for i, base_document in enumerate(documents):
        base_embeddings = vectors[i]

        scores = cosine_similarity([base_embeddings], vectors).flatten()
        output = []
        for i in range(len(scores)):
            if documents[i] != base_document:
                output.append((scores[i], documents[i], doc_ids[documents[i]]))
        output.sort(reverse=True)
        for i in range(len(output)):
            output[i] = [str(output[i][0]), output[i][1], output[i][2]]
        results[doc_ids[base_document]] = output[:20]
    json_object = json.dumps(results, indent=4)

    # Writing to sample.json
    with open("results.json", "w") as outfile:
        outfile.write(json_object)

process_bert_similarity()
