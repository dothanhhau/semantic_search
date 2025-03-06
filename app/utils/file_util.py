import os
from dotenv import load_dotenv
import numpy as np
import json
from app.utils.convert_data import format_type_of_filename

load_dotenv()

def ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Chuyển ndarray thành list
    raise TypeError(f"Object of type {obj.__class__.__name__} is not serializable")

def is_pdf_file(filename):
    return filename.lower().endswith('.pdf')

def is_json_file(filename):
    return filename.lower().endswith('.json')

def is_txt_file(filename):
    return filename.lower().endswith('.txt')

def write_file(folder, filename, type_of_file, data):
    filename = format_type_of_filename(filename, type_of_file)
    if type_of_file == 'txt':
        print()
    elif type_of_file == 'pdf':
        print()
    elif type_of_file == 'json':
        try:
            with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
                json.dump(data, f, default=ndarray_to_list, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print("Err: ", e)
            return False

def read_file(folder, filename, type_of_file):
    if type_of_file == 'txt':
        try:
            content = ''
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print('Err', e)
            return ''
    elif type_of_file == 'json':
        try:
            data = []
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print('Err', e)
            return []