from collections import OrderedDict
import torch
from transformers import AutoModel, AutoTokenizer
pretrained = 'allenai/scibert_scivocab_uncased'
# Define two models to compare
model1 = AutoModel.from_pretrained(pretrained)

# Load the state_dict of each model
model1_state_dict = model1.state_dict()
device = torch.device('mps:0')

state_dict = torch.load('/Users/adit/GameOfPapers/bert-based-triplet/ckpt/scibert_model_v6_triplet_2.pt')
state_dict = OrderedDict([(k.replace("bert.",""),v) for k, v in state_dict.items()])
del state_dict['space_joiner.out1.weight']
del state_dict["space_joiner.out1.bias"]
del state_dict["space_joiner.out2.weight"] 
del state_dict["space_joiner.out2.bias"]
model1_state_dict = {k: v.to(device) for k, v in model1_state_dict.items()}
model2_state_dict = {k: v.to(device) for k, v in state_dict.items()}
# Compare the state_dict of the two models
for key1, key2 in zip(model1_state_dict.keys(), model2_state_dict.keys()):
    # Check if the keys match

    if key1 != key2:
        print(f"Key mismatch: {key1} != {key2}")
    else:
        # Compare the values of the corresponding keys
        value1 = model1_state_dict[key1]
        value2 = model2_state_dict[key2]
        if not torch.equal(value1, value2):
            print(f"Value mismatch for key {key1}")
        else:
            print(True)