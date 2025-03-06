from flask import Blueprint, jsonify, request
from app.models.document_parts_model import DocumentParts
from app.services.tokenizer_service import vectorize_text

document_parts_bp = Blueprint('document_parts', __name__, url_prefix='/api/document_parts')

@document_parts_bp.route('/partition/<id>', methods=['GET'])
def get_document_by_partition(id):
    data = DocumentParts.get_data_by_partition_id(id)
    res = sorted(data, key=lambda x: x['key'])
    return jsonify(res)

@document_parts_bp.route('/<id>', methods=['GET'])
def get_document_by_id(id):
    id = str(id)
    data = DocumentParts.find_by_id(id)
    data[0]['vector'] = []
    print(data)
    return jsonify(data[0])

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


