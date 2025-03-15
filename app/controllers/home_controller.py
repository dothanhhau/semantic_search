from flask import Blueprint, render_template, request, jsonify
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.tokenizer_service import vectorize_text
from app.utils.convert_data import format_type_of_filename

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/', methods=['GET'])
def home():
    return render_template('trangchu.html', title="Tìm kiếm ngữ nghĩa")

@home_bp.route('/admin', methods=['GET'])
def admin():
    # return render_template('quanly.html', title="Trang quản trị viên")
    return render_template('test.html', title="Trang quản trị viên")

@home_bp.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        partitions = data['partitions']
        vector = vectorize_text(data['question'])
        if len(partitions) > 0:
            res = DocumentParts.search_on_partition([vector], partitions, 5)
        else:
            res = DocumentParts.search_all([vector], 5)
        ans = []
        for x in res:
            for y in x:
                doc = Document.find_by_id(y['entity']['doc_id'])[0]
                tmp = DocumentParts.get_childs(y['id'])
                y['entity']['doc_name'] = doc['name']
                y['entity']['file_name'] = format_type_of_filename(doc['file_name'], 'pdf')
                y['entity']['position'] = ' '.join(tmp['position'])
                y['entity']['id'] = tmp['id']
                y['entity']['page'] = tmp['page']
                y['entity']['content'] = tmp['content']
                y['entity']['distance'] = y['distance']

                ans.append(y['entity'])
                
        # Nếu <= rank4 thì gọi hàm con
        # Ngược lại tìm id cha gần nhất có rank <= 4 rồi làm lại bước trên
        
        return jsonify(ans)
    
    except Exception as e:
        print("Lỗi", e)

@home_bp.route('/show', methods=['GET'])
def show():
    file = request.args.get('file', '')
    page = request.args.get('page', 1)

    return render_template('show_pdf.html', file=file, page=page)
