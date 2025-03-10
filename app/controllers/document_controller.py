from flask import Blueprint, request
from app.models.document_model import Document
from app.models.document_parts_model import DocumentParts
from app.utils.convert_data import format_type_of_filename
from app.services.tokenizer_service import vectorize_text

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@documents_bp.route('/', methods=['GET'])
def get_all():
    data = Document.get_all()
    for x in data:
        x['file_name'] = format_type_of_filename(x['file_name'], 'pdf')
    return data

@documents_bp.route('/<id>', methods=['GET'])
def get_document_by_id(id):
    data = Document.find_by_id(id)
    res = None
    if data:
        res = data[0]
        res['file_name'] = format_type_of_filename(res['file_name'], 'pdf')
    return res

@documents_bp.route('/update', methods=['PATCH'])
def update_document_by_id():
    data = request.get_json()
    res = Document.find_by_id(data['id'])

    if len(res):
        entity = res[0]
        if data.get('file_name'):
            entity['file_name'] = data.get('file_name').strip()

        if data.get('name'):
            data['name'] = data['name'].strip()
            if entity['name'] != data['name']:
                entity['name'] = data['name']
                entity['vector'] = vectorize_text(data['name'])

        if Document.upsert(entity):
            return {"status": 200, "message": "Cập nhật thành công"}
        else:
            return {"status": 500, "message": "Cập nhật thất bại"}
    else:
        return {"status": 404, "message": "ID không tồn tại"}

@documents_bp.route('/delete/<id>', methods=['DELETE'])
def delete_document_by_id(id):
    id = str(id)
    data = Document.find_by_id(id)
    if data:
        Document.delete_by_id(id)
        if DocumentParts.drop_partition(id):
            return {"status": 200, "message": "Xoá thành công"}
        else:
            return {"status": 500, "message": "Xoá thất bại"}
    else:
        return {"status": 404, "message": "ID không tồn tại"}

