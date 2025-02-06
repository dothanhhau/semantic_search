import torch
import numpy
from app.__init__ import phoBert, phoBertTokenizer

def vectorize_sentence(sentence):
    inputs = phoBertTokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=256)
    with torch.no_grad():
        outputs = phoBert(**inputs)
    last_hidden_state = outputs.last_hidden_state
    mean_tensor = torch.mean(last_hidden_state, dim=[1, 0])
    return mean_tensor.numpy()

def vectorize_text(sentences):
    vectors_of_text = numpy.array([vectorize_sentence(sentence) for sentence in sentences])
    return numpy.mean(vectors_of_text, axis=0)