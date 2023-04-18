from transformers import AutoModel, AutoTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")

model = AutoModel.from_pretrained("adit-negi/recommendor-bert")
#model = SentenceTransformer(pretrained)


base_document = "Modeling the purposeful behavior of imperfect agents from a small number of observations is a challenging task. When restricted to the single-agent decision-theoretic setting, inverse optimal control techniques assume that observed behavior is an approximately optimal solution to an unknown decision problem. These techniques learn a utility function that explains the example behavior and can then be used to accurately predict or imitate future behavior in similar observed or unobserved situations. \nIn this work, we consider similar tasks in competitive and cooperative multi-agent domains. Here, unlike single-agent settings, a player cannot myopically maximize its reward; it must speculate on how the other agents may act to influence the game's outcome. Employing the game-theoretic notion of regret and the principle of maximum entropy, we introduce a technique for predicting and generalizing behavior."


tokens = tokenizer([base_document], padding=True, truncation=True, return_tensors="pt", max_length=500)

with torch.no_grad():
    outputs = model(**tokens)
    base_embeddings_sentences = outputs.last_hidden_state.mean(dim=1)

vectors = []
documents = ["sample document 1", "sample document 2", "sample document 3"]

for i, document in enumerate(documents):

    
    tokens = tokenizer(document, padding=True, truncation=True, return_tensors="pt", max_length=500)
    with torch.no_grad():

        outputs = model(**tokens)
        embeddings_sentences = outputs.last_hidden_state.mean(dim=1)
        
    embeddings = np.mean(np.array(embeddings_sentences), axis=0)

    vectors.append(embeddings)

scores = cosine_similarity([base_embeddings], vectors).flatten()
print (scores)