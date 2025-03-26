from app import word_dict
import string
import re

def clean_text(text):
    # Thay thế dấu câu bằng khoảng trắng
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    
    # Loại bỏ khoảng trắng thừa và chuyển về chữ thường
    text = re.sub(r'\s+', ' ', text).strip().lower()
    
    return text

def verify_question(question: str):
    question = clean_text(question)
    arr = question.split(' ')
    if len(arr) < 2: return False
    cnt = 0
    for x in arr:
        if x not in word_dict:
            cnt += 1
    return (cnt*2 < len(arr))