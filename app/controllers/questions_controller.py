import uuid
from flask import Blueprint, request
from app.models.questions_model import Questions
from app.services.tokenizer_service import vectorize_text

questions_bp = Blueprint('questions', __name__, url_prefix='/api/questions')

@questions_bp.route('/', methods=['GET'])
def get_all():
    data = Questions.get_all()
    return data

@questions_bp.route('/<id>', methods=['GET'])
def get_question_by_id(id):
    data = Questions.find_by_id(id)
    res = None
    if data:
        res = data[0]
    return res

@questions_bp.route('/create', methods=['POST'])
def create_question():
    data = request.get_json()
    Questions.insert({
        "id": str(uuid.uuid4()).replace('-', '_'),
        "content": data['content'],
        'vector': vectorize_text(data['content']),
        "rating": data['rating'],
        "feedback": data.get('feedback', '')
    })

@questions_bp.route('/update/<id>', methods=['PATCH'])
def update_question_by_id(id):
    id = str(id)
    data = request.get_json()
    res = Questions.find_by_id(id)

    return ''

@questions_bp.route('/delete/<id>', methods=['DELETE'])
def delete_question_by_id(id):
    id = str(id)
    data = Questions.find_by_id(id)

    if data:
        Questions.delete_by_id(id)
        return {"status": 200, "message": "Xoá thành công"}
    else:
        return {"status": 404, "message": "ID không tồn tại"}

