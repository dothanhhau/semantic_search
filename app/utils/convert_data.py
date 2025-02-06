# import json
# import datetime

def convert_to_json(data):
    result = {
        "ds_chuong": []
    }
    cur_chuong = {
        "ds_dieu": []
    }
    cur_dieu = {
        "ds_khoang": []
    }
    cur_khoang = {
        "ds_diem": []
    }
    
    for item in data:
        if item.startswith("Chương") or item.startswith('CHƯƠNG'):
            if cur_chuong.get("chuong"): # if có key chương rồi mà gặp key chương tiếp theo thì append vào result, else thì tạo ra key chuong
                if cur_khoang.get('khoang'):
                    cur_dieu['ds_khoang'].append(cur_khoang)

                if cur_dieu.get('dieu'):
                    cur_chuong['ds_dieu'].append(cur_dieu)

                result['ds_chuong'].append(cur_chuong)
                cur_chuong = {
                    "chuong": item,
                    "ds_dieu": []
                }
                cur_dieu = {
                    "ds_khoang": []
                }
                cur_khoang = {
                    "ds_diem": []
                }
            else:
                cur_chuong['chuong'] = item

        elif item.startswith("Điều"): 
            if cur_dieu.get("dieu"): # if có điều rồi mà gặp điều tiếp theo thì thêm điều này vào chương, else tạo ra key dieu
                if cur_khoang.get("khoang"): # if trước điều là 1 khoảng thì thêm khoảng vào điều trước, rồi mới thêm vào chương
                    cur_dieu['ds_khoang'].append(cur_khoang)
                    cur_khoang = {
                        "ds_diem": []
                    }

                cur_chuong['ds_dieu'].append(cur_dieu)
                cur_dieu = {
                    "dieu": item,
                    "ds_khoang": []
                }
            else:
                cur_dieu['dieu'] = item

        else:
            try:
                check = int(item[0])
                if cur_khoang.get("khoang"):
                    cur_dieu['ds_khoang'].append(cur_khoang)
                    cur_khoang = {
                        "khoang": item,
                        "ds_diem": []
                    }
                else:
                    cur_khoang['khoang'] = item

            except ValueError:
                cur_khoang['ds_diem'].append( {"diem": item} )

    if cur_chuong.get("chuong"): # if có key chương rồi mà gặp key chương tiếp theo thì append vào result, else thì tạo ra key chuong
        if cur_khoang.get('khoang'):
            cur_dieu['ds_khoang'].append(cur_khoang)

        if cur_dieu.get('dieu'):
            cur_chuong['ds_dieu'].append(cur_dieu)

        result['ds_chuong'].append(cur_chuong)
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
            for khoan in dieu["ds_khoang"]:
                result.append(khoan["khoang"])
                for diem in khoan["ds_diem"]:
                    result.append(diem["diem"])
    return result