# import json
# import datetime

def chuong_dieu_khoan_diem_to_json(arr):
    result = {
        "ds_chuong": []
    }
    cur_chuong = {
        "ds_dieu": []
    }
    cur_dieu = {
        "ds_khoan": []
    }
    cur_khoan = {
        "ds_diem": []
    }
    
    for item in arr:
        item = item.strip()
        if not item: continue
        if item.startswith("Chương") or item.startswith('CHƯƠNG'):
            if cur_chuong.get("chuong"): # if có key chương rồi mà gặp key chương tiếp theo thì append vào result, else thì tạo ra key chuong
                if cur_khoan.get('khoan'):
                    cur_dieu['ds_khoan'].append(cur_khoan)

                if cur_dieu.get('dieu'):
                    cur_chuong['ds_dieu'].append(cur_dieu)

                result['ds_chuong'].append(cur_chuong)
                cur_chuong = {
                    "chuong": item,
                    "ds_dieu": []
                }
                cur_dieu = {
                    "ds_khoan": []
                }
                cur_khoan = {
                    "ds_diem": []
                }
            else:
                cur_chuong['chuong'] = item

        elif item.startswith("Điều"): 
            if cur_dieu.get("dieu"): # if có điều rồi mà gặp điều tiếp theo thì thêm điều này vào chương, else tạo ra key dieu
                if cur_khoan.get("khoan"): # if trước điều là 1 khoảng thì thêm khoảng vào điều trước, rồi mới thêm vào chương
                    cur_dieu['ds_khoan'].append(cur_khoan)
                    cur_khoan = {
                        "ds_diem": []
                    }

                cur_chuong['ds_dieu'].append(cur_dieu)
                cur_dieu = {
                    "dieu": item,
                    "ds_khoan": []
                }
            else:
                cur_dieu['dieu'] = item

        else:
            try:
                check = int(item[0])
                if cur_khoan.get("khoan"):
                    cur_dieu['ds_khoan'].append(cur_khoan)
                    cur_khoan = {
                        "khoan": item,
                        "ds_diem": []
                    }
                else:
                    cur_khoan['khoan'] = item

            except ValueError:
                if not cur_khoan.get("khoan"):
                    cur_khoan['khoan'] = item
                else:
                    cur_khoan['ds_diem'].append( {"diem": item} )

    if cur_chuong.get("chuong"): # chương cuối
        if cur_khoan.get('khoan'):
            cur_dieu['ds_khoan'].append(cur_khoan)

        if cur_dieu.get('dieu'):
            cur_chuong['ds_dieu'].append(cur_dieu)

        result['ds_chuong'].append(cur_chuong)
    return result


def dieu_khoan_diem_to_json(arr):
    result = {
        "ds_dieu": []
    }
    cur_dieu = {
        "ds_khoan": []
    }
    cur_khoan = {
        "ds_diem": []
    }
    
    for item in arr:
        if item.startswith("Điều"): 
            if cur_dieu.get("dieu"): # if có điều rồi mà gặp điều tiếp theo thì thêm điều này vào chương, else tạo ra key dieu
                if cur_khoan.get("khoan"): # if trước điều là 1 khoảng thì thêm khoảng vào điều trước, rồi mới thêm vào chương
                    cur_dieu['ds_khoan'].append(cur_khoan)
                    cur_khoan = {
                        "ds_diem": []
                    }
                
                result['ds_dieu'].append(cur_dieu)

                cur_dieu = {
                    "dieu": item,
                    "ds_khoan": []
                }
            else:
                cur_dieu['dieu'] = item

        else:
            try:
                check = int(item[0])
                if cur_khoan.get("khoan"):
                    cur_dieu['ds_khoan'].append(cur_khoan)
                    cur_khoan = {
                        "khoan": item,
                        "ds_diem": []
                    }
                else:
                    cur_khoan['khoan'] = item

            except ValueError:
                if not cur_khoan.get("khoan"):
                    cur_khoan['khoan'] = item
                else:
                    cur_khoan['ds_diem'].append( {"diem": item} )

    if cur_dieu.get('dieu'):
        if cur_khoan.get('khoan'):
            cur_dieu['ds_khoan'].append(cur_khoan)
        result['ds_dieu'].append(cur_dieu)

    return result

def khoan_to_json(arr):
    result = {
        "ds_khoan": []
    }
    cur_khoan = {
        "ds_diem": []
    }
    
    for item in arr:
        try:
            check = int(item[0])
            if cur_khoan.get("khoan"):
                result['ds_khoan'].append(cur_khoan)
                cur_khoan = {
                    "khoan": item,
                    "ds_diem": []
                }
            else:
                cur_khoan['khoan'] = item

        except ValueError:
            if not cur_khoan.get("khoan"):
                cur_khoan['khoan'] = item
            else:
                cur_khoan['ds_diem'].append( {"diem": item} )
        
    if cur_khoan.get('khoan'):
        result['ds_khoan'].append(cur_khoan)
    return result

def bang_to_json(arr):
    result = ''
    
    return result

def preProcess(data):
    res = []
    for x in data:
        tmp = x.split('\n')
        u = []
        for y in tmp:
            if len(y.strip()) <= 2: continue
            u.append(y)
        if len(u):
            res.append(' '.join(u))  

    for i in range(len(res)):
        if res[i].startswith("Chương") or res[i].startswith("CHƯƠNG"):
            return res[i:]
    return []

def convertJsonDataSourceToArray(jsonData):
    result = [jsonData['tailieu']]
    for chuong in jsonData["ds_chuong"]:
        result.append(chuong["chuong"])
        for dieu in chuong["ds_dieu"]:
            result.append(dieu["dieu"])
            for khoan in dieu["ds_khoan"]:
                result.append(khoan["khoan"])
                for diem in khoan["ds_diem"]:
                    result.append(diem["diem"])
    return result


import os
from datetime import datetime
import json
folder_path = 'D:/WorkSpace/python/vector/DocSearch-Processor/quy_dinh_quy_che/txt/all/'

import re

def get_rank(x):
    re_ranks = [
        r"\$\$\$",            # Kiểm tra ký tự $$$
        r"[cC]hương\s.+:",  # Kiểm tra chữ "Chương"
        r"[IVXLCDM]+\.",     # Kiểm tra số La Mã (I. II. III. ...)
        r"[đĐ]iều\s.+\.",   # Kiểm tra chữ "Điều"
        r"truonghopdacbiet",
        r"\d+\.\s",            # Kiểm tra dạng số nguyên "1."
        r"\d+\.\d+\.",       # Kiểm tra dạng số thập phân "1.1."
        r"[a-zA-Záàảãạâấầẩẫặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]\)",  # Kiểm tra các ký tự A-Z, a-z, có dấu và ký tự kết thúc bằng ")"
        r"[a-zA-Záàảãạâấầẩẫặéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]\.",  # Kiểm tra các ký tự A-Z, a-z, có dấu và ký tự kết thúc bằng "."
    ]
    
    for index, re_rank in enumerate(re_ranks):
        if re.match(re_rank, x):
            return index
    return 1000


import uuid

def array2json(data):
    data = reversed(data)
    stack = []
    
    for entity in data:
        if not entity: continue
        # print(entity)
        id = str(uuid.uuid4())
        subs = []
        sub_ids = []
        cur_rank = get_rank(entity)

        if cur_rank == 6:
            if cur_rank != stack[-1]['rank']:
                cur = int(entity.split('.')[0])
                try:
                    pre = int(stack[-1]['content'].split('.')[0])
                    # print(pre, cur)
                    if pre - cur < 1:
                        cur_rank -= 2
                        # print(entity, cur_rank)
                except Exception as e:
                    print(e)

        while len(stack) > 0 and stack[-1]['rank'] > cur_rank:
            subs.append(stack.pop())

        res = {'id': id, 'rank': cur_rank}
        
        if cur_rank == 3:
            if '$' in entity:
                res['page'] = int(entity.split('$')[1].strip())
                res['content'] = entity.split('$')[0].strip()
            else: res['content'] = entity
        else:
            res['content'] = entity
        
        if len(subs) > 0:
            sub_ids = [sub['id'] for sub in subs]
            res['childs'] = subs
            res['child_ids'] = sub_ids

        stack.append(res)
    
    result = []
    for x in reversed(stack):
        result.append(x)
    return result


def one(file):
    with open(file, 'r', encoding='utf-8') as f:
        extract_text = f.read()

    uu = extract_text.split('\n\n\n')

    xx = []
    for x in uu:
        xx += x.split('\n\n')

    content = xx
    finalJson = array2json(content) # Chuyển từ mảng sang json với cấu trúc định sẵn
    
    path_json = 'D:/WorkSpace/python/vector/DocSearch-Processor/quy_dinh_quy_che/json/all/' + file[file.rfind('/'):-4] + '.json'
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

# def all1():
#     arr = os.listdir(folder_path)
#     for i in range(len(arr)):
#         file = arr[i]
#         file_path = folder_path + file


#         typeFile = file[-4:]
#         if typeFile != '.txt': continue

#         with open(file_path, 'r', encoding='utf-8') as f:


all()

# one('D:/WorkSpace/python/vector/DocSearch-Processor/quy_dinh_quy_che/txt/bang/chuong_dieu_khoan_diem/QD712 Quy dinh khao sat y kien cac ben lien quan 2024.txt')