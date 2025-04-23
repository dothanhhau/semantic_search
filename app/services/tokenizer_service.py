import torch
import numpy
from app import phoBert, phoBertTokenizer, vncorenlp
import re

# Hàm xóa các ký tự không mong muốn
def remove_unwanted_chars(text):
    return re.sub(r"[()\-;:,\[\]\/\+×&]", "", text).lower()

def vectorize_text(text):
    try:
        arr_txt = vncorenlp.word_segment(remove_unwanted_chars(text))
        inputs = phoBertTokenizer(arr_txt, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = phoBert(**inputs)
        last_hidden_state = outputs.last_hidden_state.mean(dim=[1, 0])
        return last_hidden_state.cpu().numpy()
    except Exception as e:
        print(e)
        return []