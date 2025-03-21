import re
import os
import uuid
import json
from datetime import datetime
from app.services.tokenizer_service import vectorize_text
folder_path = 'D:/WorkSpace/python/semantic_search/app/static/quy_dinh_quy_che/txt/'

re_ranks = [
    r"\$\$\$",            # Kiểm tra ký tự $$$
    r"[cC]hương\s.+:",  # Kiểm tra chữ "Chương"
    r"[IVXLCDM]+\.",     # Kiểm tra số La Mã (I. II. III. ...)
    r"[đĐ]iều\s\d+\.?",   # Kiểm tra chữ "Điều" theo sau là số, có thể có dấu chấm
    r"truonghopdacbiet",
    r"\d+\.\s",            # Kiểm tra dạng số nguyên "1."
    r"\d+\.\d+\.",       # Kiểm tra dạng số thập phân "1.1."
    r"[a-zA-Záàảãạâấầẩẫặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]\)",  # Kiểm tra các ký tự A-Z, a-z, có dấu và ký tự kết thúc bằng ")"
    r"[a-zA-Záàảãạâấầẩẫặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]\.",  # Kiểm tra các ký tự A-Z, a-z, có dấu và ký tự kết thúc bằng "."
]

def get_rank(x):    
    for index, re_rank in enumerate(re_ranks):
        if re.match(re_rank, x):
            return index
    return 1000

def array2json(data):
    data = reversed(data)
    stack = []
    page = None
    
    for entity in data:
        entity = entity.strip()

        try:
            page = int(entity)
        except Exception as e:
            if not entity: continue
            
            id = str(uuid.uuid4()).replace("-", "_")
            subs = []
            sub_ids = []
            cur_rank = get_rank(entity)

            if cur_rank == 6:
                if cur_rank != stack[-1]['rank']:
                    cur = int(entity.split('.')[0])
                    try:
                        pre = int(stack[-1]['content'].split('.')[0])
                        if pre - cur < 1:
                            cur_rank -= 2
                    except Exception as e:
                        if stack[-1]['rank'] < 4:
                            cur_rank -= 2
                        print(e)

            while len(stack) > 0 and stack[-1]['rank'] > cur_rank:
                subs.append(stack.pop())

            res = {'id': id, 'rank': cur_rank, 'page': page, 'content': entity}

            sub_ids = [sub['id'] for sub in subs]
            res['childs'] = subs
            res['child_ids'] = sub_ids

            if len(subs) > 0:
                for sub in subs:
                    sub['parents_id'] = id
            else:
                res['parents_id'] = id

            stack.append(res)
    
    result = []
    for x in reversed(stack):
        x['parents_id'] = x['id']
        result.append(x)
    return result

def one(file):
    with open(file, 'r', encoding='utf-8') as f:
        extract_text = f.read()

    content = extract_text.split('\n\n')
    finalJson = array2json(content) # Chuyển từ mảng sang json với cấu trúc định sẵn
    
    path_json = 'D:/WorkSpace/python/semantic_search/app/static/quy_dinh_quy_che/json/' + file[file.rfind('/'):-4] + '.json'
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(finalJson, f, ensure_ascii=False, indent=4)

    print("Dữ liệu đã được lưu vào file ", path_json)

def all():
    arr = os.listdir(folder_path)
    for i in range(len(arr)):
        file = arr[i]
        file_path = folder_path + file

        typeFile = file[-4:]
        if typeFile != '.txt': continue

        one(file_path)


def add_fields_vector_and_position(data, position=None):
    if position is None:
        position = []  # Đảm bảo mỗi lời gọi có danh sách riêng
    
    for item in data:
        item['vector'] = vectorize_text(item['content'])
        rank = item['rank']
        new_position = position.copy()  # Tạo bản sao để tránh thay đổi danh sách gốc
        
        if rank == 4:
            rank += 2
        
        if rank != 1000:
            if rank == 0:
                new_position.append(item['content'].split('$$$')[1].strip())
            else:
                match = re.search(re_ranks[rank], item['content'])
                if match:
                    new_position.append(match.group())
        
        item['position'] = new_position
        
        if 'childs' in item:
            add_fields_vector_and_position(item['childs'], new_position)
    
    return data

def add_fields_doc_id(data, doc_id):
    for index, item in enumerate(data):
        item['doc_id'] = doc_id
        item['key'] = index
    return data

def json2array(data, result=None):
    if result is None:
        result = []

    for item in data:
        flattened_item = item.copy()
        flattened_item.pop('childs', None)
        
        result.append(flattened_item)

        if 'childs' in item:
            json2array(item['childs'], result)

    return result

def select_fields_to_save_array(array):
    res = []
    for x in array:
        res.append({
            'id': x['id'], 
            'rank': x['rank'],
            'content': x['content']
        })
    return res


def datetime2string(date: datetime):
    return date.strftime('%Y-%m-%d_%H-%M-%S')

def format_type_of_filename(filename, type_of_file=''):
    filename = filename.replace(".txt", "")
    filename = filename.replace(".pdf", "")
    filename = filename.replace(".json", "")
    if type_of_file == 'txt':
        filename += '.txt'
    elif type_of_file == 'pdf':
        filename += '.pdf'
    elif type_of_file == 'json':
        filename += '.json'

    return filename

# all()
# print(os.getcwd())