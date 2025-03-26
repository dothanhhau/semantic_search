from flask import Blueprint, jsonify, request
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.tokenizer_service import vectorize_text
from app.utils.convert_data import add_fields_doc_id, add_fields_vector_and_position, array2json, json2array
from dotenv import load_dotenv

load_dotenv()

document_parts_bp = Blueprint('document_parts', __name__, url_prefix='/api/document_parts')

@document_parts_bp.route('/<id>', methods=['GET'])
def get_document_by_id(id):
    id = str(id)
    data = DocumentParts.find_by_id(id)
    if len(data):
        data[0]['vector'] = []
        return jsonify(data[0])
    else:
        return jsonify(status=404, message='ID not found!')
    

@document_parts_bp.route('/create', methods=['POST'])
def create_entity():
    
    return ''

@document_parts_bp.route('/partition/<id>', methods=['GET'])
def get_document_by_partition(id):
    data = DocumentParts.get_data_by_partition_id(id)
    res = sorted(data, key=lambda x: x['key'])
    return jsonify(res)

@document_parts_bp.route('/parents/<id>', methods=['GET'])
def find_parent(id):
    id = str(id)
    return jsonify(DocumentParts.find_parent_id_has_rank_el_4(id))

@document_parts_bp.route('/childs/<id>', methods=['GET'])
def get_childs(id):
    id = str(id)
    data = DocumentParts.get_all_child_by_id(id)
    res = sorted(data, key=lambda x: x['key'])
    content = ''
    for x in res:
        content += x['content']
        content += '\n'
    parents = res[0]
    return jsonify(
        id = parents['id'],
        content = content,
        doc_id = parents['doc_id'],
        page = parents['page'],
        position = parents['position']
    )

@document_parts_bp.route('/restructure/<id>', methods=['POST'])
def restructure(id):
    try:
        id = str(id)
        doc = Document.find_by_id(id)
        content = request.get_json()['content']
        DocumentParts.drop_partition(id)
        # write_file(os.path.join(os.getenv('UPLOAD_FOLDER'), 'txt'), doc['file_name'], 'txt', content)
        arr = content.split('\n\n')
        # Xử lý dữ liệu
        json_structer = array2json(arr)
        final_json = add_fields_vector_and_position(json_structer)
        array = json2array(final_json)
        final_array = add_fields_doc_id(array, id)
        if DocumentParts.create_partition(id):
            DocumentParts.insert(final_array, id)

        return jsonify({
            'status': 'Thành công'
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            'status': f'Xử lý thất bại: {str(e)}'
        }), 500  # Trả về lỗi 500 nếu có lỗi trong quá trình xử lý


@document_parts_bp.route('/update/<id>', methods=['PATCH'])
def update_document_by_id(id):
    try:
        id = str(id)
        data = request.get_json()
        res = DocumentParts.find_by_id(id)
        res[0]['vector'] = vectorize_text(data['content'].strip())
        res[0]['content'] = data['content'].strip()
        DocumentParts.upsert(res[0])
        return jsonify(status= 200, message="Cập nhật thành công", data=res[0]['rank'])
    except Exception as e:
        print("Lỗi: ", e)
        return jsonify(status=500, message="Cập nhật thất bại", data=1000)
    
@document_parts_bp.route('/delete/<id>', methods=['DELETE'])
def delete_document_by_id(id):
    try:
        id = str(id)
        res = DocumentParts.find_by_id(id)
        if len(res):
            DocumentParts.delete_one_by_id(id)
            return jsonify(status= 200, message="Cập nhật thành công")
        else:
            return jsonify(status=404, message="ID không tồn tại")
    except Exception as e:
        print("Lỗi: ", e)
        return jsonify(status=500, message="Cập nhật thất bại", data=1000)


