from transformers import AutoModel, AutoTokenizer
import torch
from collections import OrderedDict
def save_model():
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
    model.save_pretrained('/Users/adit/finetuned_model')

save_model()