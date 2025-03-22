import torch
import numpy
from app import phoBert, phoBertTokenizer, vncorenlp

def vectorize_text(text):
    arr_txt = vncorenlp.word_segment(text.lower())
    inputs = phoBertTokenizer(arr_txt, return_tensors="pt", padding=True, truncation=True, max_length=256)
    with torch.no_grad():
        outputs = phoBert(**inputs)
    last_hidden_state = outputs.last_hidden_state.mean(dim=[1, 0])
    return last_hidden_state.cpu().numpy()