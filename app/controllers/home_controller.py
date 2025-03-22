from flask import Blueprint, redirect, render_template, request, jsonify
from flask_jwt_extended import decode_token, get_jwt, verify_jwt_in_request
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.tokenizer_service import vectorize_text
from app.utils.convert_data import format_type_of_filename

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html', title="Tìm kiếm ngữ nghĩa")

@home_bp.route('/admin', methods=['GET'])
def admin():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        role = int(claims.get('role', None))
        if role != 0:
            return redirect(f'/login')

        return render_template('admin.html', title="Trang quản trị viên")
    except Exception as e:
        access_token = request.args.get('access_token')
        if access_token:
            try:
                role = int(decode_token(access_token)['role'])
                if role != 0:
                    return redirect(f'/login')
                return render_template('admin.html', title="Trang quản trị viên")
            except Exception as e:
                return redirect('/login')

        return redirect('/login')
@home_bp.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        partitions = data['partitions']
        vector = vectorize_text(data['question'])

        ans = []
        i = 0
        while len(ans) < 5:
            if len(partitions) > 0:
                res = DocumentParts.search_on_partition([vector], partitions, 5, i*5)
            else:
                res = DocumentParts.search_all([vector], 5, i*5)
            if not res[0]: break
            for x in res:
                for y in x:
                    doc = Document.find_by_id(y['entity']['doc_id'])[0]
                    if y['entity']['rank'] > 4:
                        parents = DocumentParts.find_parent_id_has_rank_el_4(y['id'])
                        if parents: y['id'] = parents['id']
                    check = False
                    for a in ans:
                        if a['id'] == y['id']:
                            check = True
                            break
                    if check: continue
                    tmp = DocumentParts.get_childs(y['id'])
                    y['entity']['doc_name'] = doc['name']
                    y['entity']['file_name'] = format_type_of_filename(doc['file_name'], 'pdf')
                    y['entity']['position'] = '-'.join(tmp['position'])
                    y['entity']['id'] = tmp['id']
                    y['entity']['page'] = tmp['page']
                    y['entity']['content'] = tmp['content']
                    y['entity']['distance'] = y['distance']

                    ans.append(y['entity'])
                    if len(ans) >= 5: break
            i += 1
        
        return jsonify(ans)
    
    except Exception as e:
        print("Lỗi", e)

@home_bp.route('/show', methods=['GET'])
def show():
    file = request.args.get('file', '')
    page = request.args.get('page', 1)

    return render_template('show_pdf.html', file=file, page=page)
